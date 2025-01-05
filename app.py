import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

# Fungsi untuk membuat lapangan NFL
def create_nfl_field():
    fig, ax = plt.subplots(figsize=(10, 6))

    # Membuat lapangan NFL
    field = patches.Rectangle((0, 0), 53.3, 100, linewidth=1, edgecolor='green', facecolor='lightgreen')
    ax.add_patch(field)

    # Membuat garis-garis lapangan
    for i in range(1, 11):
        ax.plot([0, 53.3], [i * 10, i * 10], color='white', lw=1)

    # Menambahkan garis gawang
    ax.plot([0, 0], [0, 100], color='white', lw=2)
    ax.plot([53.3, 53.3], [0, 100], color='white', lw=2)

    # Menambahkan nama-nama area
    ax.text(26.65, 2, 'End Zone', fontsize=12, ha='center', color='white', weight='bold')
    ax.text(26.65, 98, 'End Zone', fontsize=12, ha='center', color='white', weight='bold')

    return fig, ax

# Fungsi untuk menambahkan pemain dan bola
def add_players_and_ball(ax, blue_players, red_players, ball_position):
    # Menambahkan 11 pemain biru
    for player in blue_players:
        ax.scatter(player[0], player[1], c='blue', s=100, label="Blue Team")

    # Menambahkan 11 pemain merah
    for player in red_players:
        ax.scatter(player[0], player[1], c='red', s=100, label="Red Team")

    # Menambahkan bola
    ax.scatter(ball_position[0], ball_position[1], c='white', s=200, marker='o', label="Ball")

# Menampilkan lapangan dan pemain di Streamlit
def display_field():
    st.title("NFL Field Simulation")

    # Inisialisasi posisi pemain dan bola
    blue_players = [(random.uniform(0, 53.3), random.uniform(0, 100)) for _ in range(11)]
    red_players = [(random.uniform(0, 53.3), random.uniform(0, 100)) for _ in range(11)]
    ball_position = (random.uniform(0, 53.3), random.uniform(0, 100))

    # Input posisi baru untuk masing-masing pemain
    st.header("Move Players (1-11)")
    
    # Input posisi untuk pemain biru
    st.subheader("Blue Team")
    blue_players_input = []
    for i in range(11):
        x_pos = st.number_input(f"Player {i+1} X Position (Blue Team)", min_value=0.0, max_value=53.3, value=blue_players[i][0], step=0.1)
        y_pos = st.number_input(f"Player {i+1} Y Position (Blue Team)", min_value=0.0, max_value=100.0, value=blue_players[i][1], step=0.1)
        blue_players_input.append((x_pos, y_pos))

    # Input posisi untuk pemain merah
    st.subheader("Red Team")
    red_players_input = []
    for i in range(11):
        x_pos = st.number_input(f"Player {i+1} X Position (Red Team)", min_value=0.0, max_value=53.3, value=red_players[i][0], step=0.1)
        y_pos = st.number_input(f"Player {i+1} Y Position (Red Team)", min_value=0.0, max_value=100.0, value=red_players[i][1], step=0.1)
        red_players_input.append((x_pos, y_pos))

    # Menampilkan lapangan dan pemain di Streamlit
    fig, ax = create_nfl_field()
    add_players_and_ball(ax, blue_players_input, red_players_input, ball_position)

    ax.set_xlim(0, 53.3)
    ax.set_ylim(0, 100)
    ax.set_aspect('equal')

    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig)

# Menampilkan aplikasi
if __name__ == "__main__":
    display_field()
