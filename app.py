import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

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
    ax.text(2, 26.65, 'End Zone', fontsize=12, ha='center', color='white', weight='bold')
    ax.text(98, 26.65, 'End Zone', fontsize=12, ha='center', color='white', weight='bold')

    return fig, ax

# Fungsi untuk menambahkan pemain dan bola
def add_players_and_ball(ax, blue_players, red_players, ball_position):
    # Menambahkan 11 pemain biru dengan nomor
    for idx, player in enumerate(blue_players):
        ax.scatter(player[1], player[0], c='blue', s=100)
        ax.text(player[1], player[0], str(idx+1), color='white', ha='center', va='center', fontsize=10, weight='bold')

    # Menambahkan 11 pemain merah dengan nomor
    for idx, player in enumerate(red_players):
        ax.scatter(player[1], player[0], c='red', s=100)
        ax.text(player[1], player[0], str(idx+1), color='white', ha='center', va='center', fontsize=10, weight='bold')

    # Menambahkan bola
    ax.scatter(ball_position[1], ball_position[0], c='white', s=200, marker='o', label="Ball")

# Menambahkan keterangan garis lapangan
def add_field_labels(ax):
    labels = [10, 20, 30, 40, 50, 40, 30, 20, 10]
    for x in labels:
        ax.text(x, 53.0, str(x), color='white', ha='center', fontsize=12, weight='bold')

# Menampilkan lapangan dan pemain di Streamlit
def display_field():
    st.title("NFL Field Simulation")

    # Input posisi untuk Blue Team di sidebar
    st.sidebar.header("Blue Team")
    blue_players_input = []
    # Menyusun pemain biru di sebelah kiri
    for i in range(11):
        x_pos = st.sidebar.number_input(f"Player {i+1} X Position (Blue Team)", min_value=0.0, max_value=50.0, value=10.0, step=0.1)
        y_pos = st.sidebar.number_input(f"Player {i+1} Y Position (Blue Team)", min_value=0.0, max_value=53.3, value=(i+1)*4.5, step=0.1)  # Susun vertikal
        blue_players_input.append((y_pos, x_pos))

    # Input posisi untuk Red Team di sidebar
    st.sidebar.header("Red Team")
    red_players_input = []
    # Menyusun pemain merah di sebelah kanan
    for i in range(11):
        x_pos = st.sidebar.number_input(f"Player {i+1} X Position (Red Team)", min_value=50.0, max_value=100.0, value=90.0, step=0.1)
        y_pos = st.sidebar.number_input(f"Player {i+1} Y Position (Red Team)", min_value=0.0, max_value=53.3, value=(i+1)*4.5, step=0.1)  # Susun vertikal
        red_players_input.append((y_pos, x_pos))

    # Inisialisasi bola di posisi acak yang bisa diubah sesuai kebutuhan
    ball_position = (st.sidebar.number_input("Ball Y Position", min_value=0.0, max_value=53.3, value=26.65, step=0.1),
                     st.sidebar.number_input("Ball X Position", min_value=0.0, max_value=100.0, value=50.0, step=0.1))

    # Menampilkan lapangan dan pemain di Streamlit
    fig, ax = create_nfl_field()
    add_players_and_ball(ax, blue_players_input, red_players_input, ball_position)
    add_field_labels(ax)  # Menambahkan keterangan garis lapangan

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 53.3)
    ax.set_aspect('equal')

    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig)

# Menampilkan aplikasi
if __name__ == "__main__":
    display_field()
