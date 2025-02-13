import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import joblib
from tensorflow.keras.models import load_model



# Fungsi untuk membuat lapangan NFL
def create_nfl_field():
    fig, ax = plt.subplots(figsize=(10, 6))

    # Membuat lapangan NFL (dalam orientasi horizontal)
    field = patches.Rectangle((0, 0), 100, 53.3, linewidth=1, edgecolor='green', facecolor='lightgreen')
    ax.add_patch(field)

    # Membuat garis-garis lapangan
    for i in range(1, 11):
        ax.plot([i * 10, i * 10], [0, 53.3], color='white', lw=1)

    # Menambahkan garis gawang
    ax.plot([0, 0], [0, 53.3], color='white', lw=2)
    ax.plot([100, 100], [0, 53.3], color='white', lw=2)

    # Menambahkan nama-nama area
    ax.text(2, 18, 'Offensive Team', fontsize=12, ha='center', color='black', weight='bold', rotation=90)
    ax.text(98, 18, 'Defensive Team', fontsize=12, ha='center', color='black', weight='bold', rotation=270)

    # Menambahkan keterangan garis lapangan dengan font warna hitam
    y_pos = 54  # Posisi teks di luar lapangan
    for i, label in zip(range(1, 10), [10, 20, 30, 40, 50, 40, 30, 20, 10]):
        ax.text(i * 10, y_pos, str(label), fontsize=10, ha='center', color='black', weight='bold')

    return fig, ax

# Fungsi untuk menambahkan pemain dan bola
def add_players_and_ball(ax, blue_players, red_players, ball_position):
    player_positions = []
    
    # Menambahkan 11 pemain biru dengan nomor dan menyimpan posisi
    for idx, player in enumerate(blue_players):
        ax.scatter(player[1], player[0], c='blue', s=100)
        ax.text(player[1], player[0], str(idx+1), color='white', ha='center', va='center', fontsize=10, weight='bold')
        player_positions.append({'Team': 'Blue', 'Player': idx+1, 'X Position': player[1], 'Y Position': player[0]})

    # Menambahkan 11 pemain merah dengan nomor dan menyimpan posisi
    for idx, player in enumerate(red_players):
        ax.scatter(player[1], player[0], c='red', s=100)
        ax.text(player[1], player[0], str(idx+1), color='white', ha='center', va='center', fontsize=10, weight='bold')
        player_positions.append({'Team': 'Red', 'Player': idx+1, 'X Position': player[1], 'Y Position': player[0]})

    # Menambahkan bola dan menyimpan posisi
    ax.scatter(ball_position[1], ball_position[0], c='white', s=200, marker='o', label="Ball")
    player_positions.append({'Team': 'Ball', 'Player': 'N/A', 'X Position': ball_position[1], 'Y Position': ball_position[0]})

    return player_positions

# Fungsi untuk menambahkan garis Yards to Go
def add_yards_to_go_line(ax, yards_to_go_x):
    ax.plot([yards_to_go_x, yards_to_go_x], [0, 50], color='orange', lw=2)
    ax.text(yards_to_go_x, 51, 'Yards to Go', fontsize=9, ha='center', color='black', weight='bold')

# Menampilkan lapangan dan pemain di Streamlit
def display_field():
    st.title("AI-Training Partner")
    

    # Input posisi untuk Blue Team di sidebar
    st.sidebar.header("Blue Team")
    blue_players_input = []
    for i in range(11):
        x_pos = st.sidebar.slider(f"Player {i+1} X Position (Blue Team)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
        y_pos = st.sidebar.slider(f"Player {i+1} Y Position (Blue Team)", min_value=0.0, max_value=53.3, value=(i+1)*4.5, step=0.1)
        blue_players_input.append((y_pos, x_pos))

    # Input posisi untuk Red Team di sidebar
    st.sidebar.header("Red Team")
    red_players_input = []
    for i in range(11):
        x_pos = st.sidebar.slider(f"Player {i+1} X Position (Red Team)", min_value=0.0, max_value=100.0, value=90.0, step=0.1)
        y_pos = st.sidebar.slider(f"Player {i+1} Y Position (Red Team)", min_value=0.0, max_value=53.3, value=(i+1)*4.5, step=0.1)
        red_players_input.append((y_pos, x_pos))

    # Inisialisasi bola di posisi acak
    ball_position = (st.sidebar.slider("Ball Y Position", min_value=0.0, max_value=53.3, value=26.65, step=0.1),
                     st.sidebar.slider("Ball X Position", min_value=0.0, max_value=100.0, value=50.0, step=0.1))

    # Input untuk Yards to Go Line
    yards_to_go_x = st.sidebar.slider("Yards to Go Line (X Position)", min_value=0, max_value=100, value=50, step=1)

    # Menampilkan lapangan dan pemain di Streamlit
    fig, ax = create_nfl_field()
    player_positions = add_players_and_ball(ax, blue_players_input, red_players_input, ball_position)
    
    # Menambahkan garis Yards to Go
    add_yards_to_go_line(ax, yards_to_go_x)

    # Membuat DataFrame untuk posisi pemain, bola, dan garis Yards to Go
    position_df = pd.DataFrame(player_positions)
    position_df['Yards to Go X Position'] = yards_to_go_x

    # Menampilkan DataFrame
    #st.write("Player and Ball Positions DataFrame:")
    #st.dataframe(position_df)

    # Menampilkan plot
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 53.3)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig)

    position = position_df[['Yards to Go X Position', 'X Position', 'Y Position']].copy()
    position['Direction'] = 1  # Menambahkan kolom Direction
    position['X Position'] = position['X Position'] + 10
    position['Yards to Go X Position'] = position['Yards to Go X Position'] + 10
    position['Yards to Go X Position'] = position['Yards to Go X Position'] - position['X Position'].iloc[22]
    position = position[['Direction', 'Yards to Go X Position', 'X Position', 'Y Position']]

    position['X Position'] = position['X Position'].astype(int)
    position['Y Position'] = position['Y Position'].astype(int)

    
    range_values = list(range(0,120))
    encoder = OneHotEncoder(categories=[range_values], sparse_output=False)
#Encode 'x' and 'y' columns
    x_io = encoder.fit_transform(position['X Position'].values.reshape(-1, 1))
    y_io = encoder.fit_transform(position['Y Position'].values.reshape(-1, 1))

# Convert to DataFrame for better readability
    x_io = pd.DataFrame(x_io, columns=[f'x_{i}' for i in range_values])
    y_io = pd.DataFrame(y_io, columns=[f'y_{i}' for i in range_values])

    #position = position[['Direction', 'Yards to Go X Position']]
    position = pd.concat([position[['Direction', 'Yards to Go X Position']], x_io, y_io], axis=1)
    data = position.to_numpy()
    # Menambahkan dimensi batch dan channel
    data = data.reshape(1, 23, 242, 1)
    #st.write(f"Reshaped data shape: {data.shape}")
    #data = data.reshape(1, -1)
    #st.write("Array:", data)
    # Menampilkan DataFrame
    #st.write("position data frame:")
    #st.dataframe(position)
    #st.write(data.shape)
    #st.write(f"Shape of data: {data.shape}")
    #model = load_model('model_test.h5')
    #st.write(f"Model input shape: {model.input_shape}")
    # melakukan prediksi 
    # Load model
    model = load_model('model_test.h5')
    #st.write(f"Model input shape: {model.input_shape}")

    # Prediksi
    if st.button("Predict"):
        try:
            prediction = model.predict(data)
            st.write(f"The winning probability of Blue team is : {prediction[0]}")
        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")

    

# Menampilkan aplikasi
if __name__ == "__main__":
    display_field()
