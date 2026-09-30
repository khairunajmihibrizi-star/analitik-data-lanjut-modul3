import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector


# =========================
# Koneksi dan Ambil Data
# =========================
def get_data_from_db():
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="db_dal"
    )

    query = """
        SELECT
            id,
            semester,
            jumlah,
            program_studi,
            universitas
        FROM pddikti_example
    """

    data = pd.read_sql(query, conn)

    # Membersihkan spasi pada nama kolom
    data.columns = data.columns.str.strip()

    conn.close()

    return data


# =========================
# Judul Aplikasi
# =========================
st.title("Streamlit Simple App")


# =========================
# Sidebar
# =========================
page = st.sidebar.radio(
    "Pilih halaman",
    ["Dataset", "Visualisasi", "Form Input"]
)


# =========================
# HALAMAN DATASET
# =========================
if page == "Dataset":

    st.header("Halaman Dataset")

    data = get_data_from_db()

    st.dataframe(
        data,
        use_container_width=True
    )


# =========================
# HALAMAN VISUALISASI
# =========================
elif page == "Visualisasi":

    st.header("Halaman Visualisasi")

    data = get_data_from_db()

    # Memilih universitas
    selected_university = st.selectbox(
        "Pilih Universitas",
        data["universitas"].dropna().unique()
    )

    # Filter berdasarkan universitas
    filtered_data = data[
        data["universitas"] == selected_university
    ]

    # Membuat grafik
    fig, ax = plt.subplots(figsize=(12, 6))

    for prog_studi in filtered_data["program_studi"].dropna().unique():

        subset = filtered_data[
            filtered_data["program_studi"] == prog_studi
        ].copy()

        # Urutkan berdasarkan ID
        subset = subset.sort_values(
            by="id",
            ascending=False
        )

        ax.plot(
            subset["semester"],
            subset["jumlah"],
            marker="o",
            label=prog_studi
        )

    ax.set_title(
        f"Visualisasi Data untuk {selected_university}"
    )

    ax.set_xlabel("Semester")
    ax.set_ylabel("Jumlah")

    plt.xticks(rotation=90)

    ax.legend()

    ax.grid(True)

    st.pyplot(fig)


# =========================
# HALAMAN FORM INPUT
# =========================
elif page == "Form Input":

    st.header("Form Input")

    with st.form("form_input"):

        semester = st.text_input(
            "Semester"
        )

        jumlah = st.number_input(
            "Jumlah",
            min_value=0,
            step=1
        )

        program_studi = st.text_input(
            "Program Studi"
        )

        universitas = st.text_input(
            "Universitas"
        )

        submit = st.form_submit_button(
            "Submit"
        )

        if submit:

            conn = mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="",
                database="db_dal"
            )

            cursor = conn.cursor()

            query = """
                INSERT INTO pddikti_example
                (
                    semester,
                    jumlah,
                    program_studi,
                    universitas
                )
                VALUES (%s, %s, %s, %s)
            """

            values = (
                semester,
                jumlah,
                program_studi,
                universitas
            )

            cursor.execute(query, values)

            conn.commit()

            cursor.close()
            conn.close()

            st.success(
                "Data successfully submitted to the database!"
            )