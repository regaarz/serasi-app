import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import paho.mqtt.client as mqtt


# MQTT Settings
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPICS = {
    "tds": "esp32/hydrats/innovillage/tds",
    "ph": "esp32/hydrats/innovillage/ph",
    "water_temperature": "esp32/hydrats/innovillage/water_temperature",
    "turbidity": "esp32/hydrats/innovillage/turbidity",
    "water_flow": "esp32/hydrats/innovillage/water_flow",
    "distance": "esp32/hydrats/innovillage/distance",
    "water_quality": "esp32/hydrats/innovillage/water_quality",
    "tegangan": "esp32/hydrats/innovillage/tegangan"
}

sensor_data = {key: "N/A" for key in MQTT_TOPICS}

# Function to include the CSS file
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        for topic in MQTT_TOPICS.values():
            client.subscribe(topic)
        print("Connected to MQTT broker.")
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    for key, topic in MQTT_TOPICS.items():
        if msg.topic == topic:
            sensor_data[key] = msg.payload.decode("utf-8")

# Initialize MQTT Client
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

try:
    mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
    mqtt_client.loop_start()
except Exception as e:
    st.error(f"Failed to connect to MQTT broker: {e}")

# Streamlit Page Configuration
st.set_page_config(layout="wide")

st.markdown("""
<style>
/* CSS Styles for Streamlit UI */
body {
    font-family: Arial, sans-serif;
    background-color: #f9f9f9;
}

.stButton > button {
    background-color: #f2d230 !important;
    color: black !important;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    cursor: pointer;
}

.stButton > button:hover {
    background-color: #e6c020 !important;
    color: white !important;
}

.sensor-box {
    background-color: rgba(30, 144, 255, 0.85); /* Warna biru cerah */
    border-radius: 12px; /* Membuat sudut lebih membulat */
    padding: 20px; /* Jarak dalam */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Efek bayangan lembut */
    text-align: center; /* Pusatkan teks */
    font-size: 14px; /* Ukuran font */
    margin: 10px; /* Jarak antar elemen */
}
}

.sensor-title {
    font-size: 1.2em;
    color: #FFD700; /* Warna kuning emas */
    font-weight: bold;

.sensor-value {
    font-size: 1.8em;
    color: #32CD32; /* Warna hijau cerah */
    font-weight: bold;
}

.sensor-box:hover {
    transform: scale(1.05); /* Sedikit memperbesar ukuran */
    transition: transform 0.2s ease-in-out; /* Efek transisi halus */
    background-color: rgba(0, 102, 204, 0.9); /* Warna biru lebih gelap */
}

/* Animasi untuk nilai sensor */
.sensor-value {
    animation: pulse 1.5s infinite;
}

@keyframes pulse {
    0% {
        color: #32CD32; /* Hijau cerah awal */
    }
    50% {
        color: #ADFF2F; /* Hijau kekuningan di tengah */
    }
    100% {
        color: #32CD32; /* Kembali ke hijau cerah */
    }
}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <style>

    .stButton > button {
        background-color: #f2d230 !important; /* Mengubah warna button menjadi kuning */
        color: black !important; /* Warna teks pada tombol menjadi hitam */
        border: none; /* Menghilangkan border */
        border-radius: 8px; /* Membuat sudut tombol membulat */
        padding: 10px 20px; /* Menyesuaikan padding tombol */
        font-weight: bold; /* Membuat teks lebih tebal */
        cursor: pointer; /* Menjadikan kursor sebagai pointer */
    }

    .stButton > button:hover {
        background-color: #e6c020 !important; /* Warna kuning lebih gelap saat tombol di-hover */
        color: white !important; /* Teks menjadi putih saat hover */
    }

    .nav-link {
        background-color: yellow !important; /* Warna latar belakang */
        color: black !important; /* Warna teks */
        font-weight: bold !important; /* Ketebalan teks */
        border-radius: 5px !important; /* Membuat sudut sedikit melengkung */
    }
    .nav-link:hover {
        background-color: orange !important; /* Warna hover */
        color: white !important; /* Warna teks saat hover */
    }
    .nav-link-selected {
        background-color: gold !important; /* Warna saat dipilih */
        color: black !important; /* Warna teks saat dipilih */
    }

    .stButton > button {
    background-color: #f2d230 !important; /* Warna tombol kuning */
    color: black !important; /* Teks hitam */
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    cursor: pointer;
}

.stButton > button:hover {
    background-color: #e6c020 !important; /* Warna hover kuning gelap */
    color: white !important;
}



    </style>
""", unsafe_allow_html=True)
    
    # Sidebar navigation menggunakan option_menu
    menu_selection = option_menu(
        menu_title=None,
        options=["Home", "Monitoring", "About Us","FAQ"],
        icons=["house-fill", "clipboard-data-fill", "gear-wide-connected", "search"],
        default_index=0,
        orientation="horizontal",
    )

    if menu_selection == "Home":
        st.markdown("<hr/>", unsafe_allow_html=True)
        #Logo
        header_image = Image.open('Serasi2.png')  
        col1, col2, col3 = st.columns([3, 0.2, 3])  
        with col2:
            st.image(header_image, width=330)

        #Tulisan SERASI
        col1, col2, col3 = st.columns([4.3, 5 ,6])
        image2 = Image.open('Serasi5.png')
        col2.image(image2,width=370)

        #Tulisan singkatan
        header_image2 = Image.open('Serasi4.png')  
        col1, col2, col3 = st.columns([2, 2, 1])  
        with col2:
            st.image(header_image2, width=350)

        st.markdown("<hr/>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style='display: flex; justify-content: center; margin-top: 20px; margin-bottom: 20px;'>
                <p style='text-align: center; max-width: 1200px;'>
                Welcome to SERASI, where you can manage and monitor your waterc system smartly!
                Use the Topbar navigation on the left to explore our features.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns([0.2, 0.4, 0.2])
        # Muat gambar
        image_hidro = Image.open('bendungan.jpg')
        # Tampilkan gambar
        col2.image(image_hidro, use_column_width=True)

        st.markdown(
            """
            <div style='display: flex; flex-direction: column; align-items: flex-start; margin-top: 20px; margin-bottom: 20px;'>
                <p style='text-align: left;'>
                Website SERASI (Sistem Irigasi dan Pemantauan Bendungan Terintegrasi IoT) merupakan platform yang dirancang untuk mendukung keberlanjutan pengelolaan bendungan di Kampung Pasirhonje. 
                Alat ini adalah bagian dari proyek Innovillage, di mana tim kami melakukan perbaikan bendungan sekaligus mengintegrasikan teknologi IoT (Internet of Things) untuk pemantauan real-time.
                Dengan memanfaatkan teknologi IIoT (Industrial Internet of Things), PLTS (Pembangkit Listrik Tenaga Surya), dan PLTMH (Pembangkit Listrik Tenaga Mikrohidro).
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("""
<div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-top: 20px;">
    <div class="inovasi-box">
        <div class="inovasi-title">Internet of Things</div>
        <div class="inovasi-value">
            Memantau kondisi bendungan secara real-time, termasuk data suhu, pH, kualitas air, ketinggian air, kandungan air, tegangan, dan arus.
        </div>
    </div>
    <div class="inovasi-box">
        <div class="inovasi-title">Pembangkit Listrik Tenaga Surya (PLTS)</div>
        <div class="inovasi-value">
            Menggunakan energi cahaya matahari untuk menghasilkan listrik. PLTS merupakan salah satu teknologi energi terbarukan yang ramah lingkungan.
        </div>
    </div>
    <div class="inovasi-box">
        <div class="inovasi-title">Pembangkit Listrik Tenaga MikroHidro (PLTMH)</div>
        <div class="inovasi-value">
            Menggunakan aliran sungai atau irigasi sebagai sumber tenaga. PLTMH termasuk sumber energi terbarukan dan ramah lingkungan.
        </div>
    </div>
    <div class="inovasi-box">
        <div class="inovasi-title">Website Interface</div>
        <div class="inovasi-value">
            Memberikan pengguna kemampuan untuk memantau dan mengontrol kondisi air dari mana saja dan kapan saja.
        </div>
    </div>
</div>

<style>
.inovasi-box {
    background-color: #f2f2f2; /* Warna abu-abu terang */
    border-radius: 12px; /* Membuat sudut lebih membulat */
    padding: 20px; /* Jarak dalam */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Efek bayangan lembut */
    text-align: center; /* Pusatkan teks */
    font-size: 14px; /* Ukuran font */
    margin: 10px; /* Jarak antar elemen */
    width: calc(100% - 40px); /* Default untuk layar kecil */
    max-width: 300px; /* Batas maksimum lebar */
}
.inovasi-title {
    font-size: 1.2em;
    color: black; /* Warna hitam untuk judul */
    font-weight: bold;
}
.inovasi-value {
    font-size: 1em;
    color: black; /* Warna hitam untuk teks */
    font-weight: normal;
}
.inovasi-box:hover {
    transform: scale(1.05); /* Sedikit memperbesar ukuran */
    transition: transform 0.2s ease-in-out; /* Efek transisi halus */
    background-color: #e0e0e0; /* Warna abu-abu sedikit lebih gelap saat hover */
}
</style>
""", unsafe_allow_html=True)


        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            """
            <h2 style='text-align: center;'>Sustainable Development Goals (SDGs)</h2>
            """,unsafe_allow_html=True
        )
        st.markdown("<br>", unsafe_allow_html=True)

        
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
        """
        <div style="text-align: center;">
            <img src="https://bappeda.jogjaprov.go.id/dataku/static/images/sdgs/6.png" alt="SDGs 6" style="width: 200px; margin: auto;">
            <p>SDGs 6</p>
        </div>
        """, unsafe_allow_html=True
    )

        with col2:
            st.markdown(
        """
        <div style="text-align: center;">
            <img src="data:image/png;base64,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" alt="SDGs 7" style="width: 200px; margin: auto;">
            <p>SDGs 7</p>
        </div>
        """, unsafe_allow_html=True
    )

        with col3:
            st.markdown(
        """
        <div style="text-align: center;">
            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOEAAADhCAMAAAAJbSJIAAAAh1BMVEU+sEn///81rkE6r0ZlvWye06JZumKNzJEpqzc3rkMurDwsrDoxrT5Fsk+v2bCVzpi/4L/c7d4cqS1ywXm+38D0+PSk1KjP59Hp9Oq03LbX7NeGyIteuWap1qnj8eTI5MpNtVdsv3Oa0J6AxoSJyo7x+PEOpiSCx4XN580ApBhStlzF48VrvnCuuDhEAAANnklEQVR4nO2di3aqMBaGSQIaSJSboFhF1KJW+/7PN3sHRLSo2DVT4Uz+tY4HkEA+k+xLuNQwtLS0tLS0tLS0tLS0tLS0tHot5ijhou38FDvvxzmXsDf8Rw2HKzGbc2HAGnxhCI7HkGoL7CeEAzuCKOxYHoIWxSjDY8CuAj8cIZgq6OAB4Csbj6iOKYr9xXkBj84Zfl2cpJ3sxclDQUE7LBbrOoUl4sj307FkZuqnQ574qNTcpv7ccZI0loZzSCeO4Yx92AIVHR0iMnOhHtSFEqMCEBax2DBL008qrdQ3hJWTaDVihrOEBU/a6zQNbTmGlUTac3UafxqUC85SHUuc4CT8AdN1CxoRUaJYA/JTQ1rsN4Jln9Mh/BcH0+K7Na4d+ZwAG5/B1wZPYQtUWOTnwmKFO9p4DBkXxeIjIRvJCPGCsdowkyJRCyu+JWQfTNTKJCirEO3KOvKJOhaH1ShoS6iq1JYwF3JcEkaJ502OSLiBtYrQwbqENv2A2n7kZFYyu/RMOIFiWyTksDIScMzPAyFbBzA/5oQYYbGS4gpNPPgpV14SRCSF83nCUxVi5AVCfiAvEBKDr0rC2Q7GqMQCh92FkB1JlJMNlUvcdwO/uoF1J55zJhwJx6ED/F0ISTgsuByOHKsF+FgjoUnIB/8mxBTYpN/cgd9tEsDpHGzDsTBfIORj8gJhRAZBCp+KEMeBKhDV2tAOSYprEjodk0AokNkjxahBwiMMa4Y8UJTZUFdXwpGXC2B2jmn6jYQAN3QWaWoy7AuhjT3jhL8REEbQk/fw2ZJQ1JBaEM7JR0DSkjBgDAvMUnK8EFKLHBLgUYT2Oo5tewsGh0TiTJjZjCHhcEbGDluUhGPorjMOdlQioYReiitwgopwwuF8QDgnaRDDZztCuiaNhPNxctGaVYQJsSQ5FYT50TQzKJAnxD1UhFCFZAM8DhI6QRAg1TRUxqcgXC/Moz3AXwuqfiEMToRMAzTnQBjA0FkpggvhamCaSHiKIjBEXjtC6EDNhHEgLyqdBRJuyGRA4ost/YQ+kIfksKoIuU82MHQyNI0iAdMuxYl4WWlMS1s6wQEH8mptKCkYX18yRUjRvs/FFSEqExMySYn0o2U7Qp7fIVzKhp8D6hGS+ZZ8XBNGgkSnC2FEtmgvOBBy3EmAKbVoaUxvCKOgRsiyiBQDmWxt+4iIvJFwRY55GrckJC8SDkhuwUcxDo0sG0GB6GsGtvJMiDsxNItA6LhzJATmICeJUxIuoBj2UuymC3ohNGxjhtZVERr2KFcba5YGzoe9dDKG3/jwvyLMZtGE0JKQF5Ym2qGvLgkDqJ8DXSMJcBxyOJxiDuaFMS0tjbKlPgyRWFSEDqW2DS3FVC+FlVGEVaoRlpbmNARzMH6F0F++QAiOPtqRK28RBdsa4aY0Vbuzt8A2QeWBce0tNhCn+LwizCxrhN41RMKjZWXCwsH701usTJKT4bg94azyiC0Ij1Bv/+uGkBsXwt2k5EFCG2t8Ziby3IZnQrSeIyAcKn+4hqam4Ac/kTDEFfjY1wlFSQiuhCzaE+ZM3CFkVFL7lhC+P53bcCcge0BCsJ9kIgL4frqbg1UfwBE5tMDiCzCB2T8uoNyClTENF0IioYC2H6IL+gK3b8GW/dewjGmAO/yCMt81jz8J4HRgaVYYo9qtCXPGZCMhdUw3tkLmXBEO4PTx7jryjjgeYaJiug3Ej5YjoVYmVJKkyOyD6USDgoHDj8h7CmYKdyMLDKZ9bGrlD0mxIm5sKVGEEFUFbQlz8MONhDu3dCRjfk4PkXABjg2iGiCcl4RoS9DAK0LfybBnKRcQFLnCEWIVyKzAOiXQL+TyQmhRSEmI812cRtC9WvjElv0Qn2rlAyzNZ0FY1pGf4DdbkRQHQSuPj2OiiXDjkbPSSysO3ZE9dDM6dE26HaLcbOEOwbS7w9CAFucsc90M9nTdb8bXyWRj21BqADZ3OIR6Gsx0VTFz5LomgzU42siajL9hTMvjcrI8SnZ0oYAcjCfxEcfKwHXBNrFPdb6hHbqh/IZ/a7cMJp8hGs2EKbloWmWalJ7/McOmSozhBrVFSrvcp1jH+YLzd/ipxjQrixVbVWEmHVl8BwvFRlatnFeNohyF89qwyS6KtlQT4ZVC+/lBOq2nhNV0gUAVP50D9hD+o7il+K1tgbMtUhR6E0uzmgnnYy86L5fOcXRCucoteaeVBWbAXcGWZAE72NvV6QDx9qnQ6K1IN2okdAMp6OyqmxY5PrCj6SEYKhjOpNpBLWL8WWjEnpz1L9VoadASoysqcFXPRMJ0laMNZ8rEC2hKSON8oiag0H1YgXcAR+mvDp1vQ/RdVaOhPytX4wBaL3HoELIJCL+QMIAwhgBhBJtOQnLwdJ9B98dhEZeyH4SQAUD45EAC72GOg4QUwgzCiwkAaEvl7dsb8j9RnbCcET7ti5HXQAgJjueIKYGYJ5YXQntNcghRnc4TKpsPKjzgXULIIkIIsYXqpUFKUpwn9r+x43ae8Er3CAXkL0cPuJDQz9GWyoScRtXUUpcJadGG5ezaHUKcZYEsIVK9FOQzBqZ0DLnYhnadsHDhp0MxgXiX8BNSlz3mDUCY4MSf4JB2B7Pz5FmHCZ0i5cG0xbhPCMmZvwOvEPLSW0QBZEfmboqz+v8E4Q6aLY+Ugy9taQBcUR6dpwd7TYj+cFeGc5ML4bDcldk9J4y/BsUlhjgMU+iqZ0JIuWfrECfHaE8I93cII2y9NVAuJD+RqCL8mpJDQDOcGew4oXzShqiEf2DugJNKFOAoZhW7HENZB+fru05o1ZhYVn5hlQliDNosOFvHGxvCszjOtpbF2LcVZxvrmxl0Y33QzLLMLqVOxo0/LBMmH7Mn55wsfpZtgheiqukVNYFiq4kWWKhNxhSLXVKdsGq2ZcCDwTnJX3Styi/qKmqrkvR87pdLOG3fb10Rystl/UpJw0WMXumKkLGfhEbPO+lN9kS3t4Bhx2z/67rJD8X+BtB5Ur77Onv5cwYss1OFFyVG71uwQUw4oZV43tg1uez7GLwnmzrCkZ1z3VpaWlpaWlpaWlpaWlpaWlpaWv+4GPvFpNxvyrxDTHLOjkeDvzazSjnPjpJ3f7bZ5oNleREuTcz2FaafqlQ65N1uSMbXfv0KR7ptWWFqVUWyLjejbZ/IjeajVhWmG5Ker8SaEt8hwJ0ONiatLoLXtW51NZXCOBxZRXkznqazebLoXIfFO4OaFLa9YMzw8dmaDna3EKtbGn7IbP/8CV/WC+adur//8iKGH4peeMImuGrFWZfuiHDie4CEnF6oqICxOHUXoywcR+qx366IGfcB8Unn9gcaxCNOISayHeGVb5bohOTyEeHphact2OUqrFh36Amy6+f4f+iXXrxDhoYNHgLi4/SPRPH9RLJDDfZTjc/w1XRzExWj+Aokp0Ry5N6b+/Mk7GzczagTJI8Jr95vxMTIOkDU4m0lhGbUrsrm3Yy7pTAt7zR7xIcvXrkUsNnlkeLECK7uuJp3aegVsvG1Vc9Vc91yUY9eo5tY/dCtZ9xgCH03BduPCO2wcQd/uV0stknxNpAOqXxI/rku41BMMTeON8tTre29I1hSdPK0OzGMktzfZ7rWJTahH/4gkJJKEQzK8Zh3L08qVT1R+ly1dwHQyysZeIYP0s6dzjpCPm1NeMdEssAih6424PM4pqbp3eRCso6ZlrqabgC/I2/BO2ZCWul+ytug3LL7x8ifc13J7e6Au6OGe/gfK203s9gdvUyIryp7d6Vf0qu9FGX2CpE/ySca1a35wSeST3LCRqVdmh98JnZnjvux4j45DT7/DWL3ctz7uj+P/0hdywAfSg6fA/1Q1Kduqt57/LL69aIwsW03i1FXzx7PDNonGGf5fXIYDU9fPlf7N6d3QfJ1QHwjWH8kH1w0vK+mGX5Rf+7PVrcqdOI6xpMrTndUd4iMZ5uVP/NPm2N51YIJuU3maYrXMd5uk5j5G0BSszRicZnN8vf4VyzE6BLuRpt3J83Prjg16zL/zfi1JU4X/GbLbPDeZnR+k12QVWVp2I/AdvkjI9u+NaN0vNv6tFH1JpfiyvgsnTVGDbM0Vdvf+r5F+SvCKgmGTn5aBAHnAduvrnZJ4wHH7XSYR+8EfHJ7wh3VLpbS0fk1cJSzy7Hm39WNm/jy3HeQnXXnStljfdfcXK32zGHFn0aJtkEXHGGpX0y33f97PixA0+x365UNfPWU6FbZg14nwnz1bg94o9enaj4f+jebd24CgL9oTce9ypyUnJcmTZNeJU6F2OiFJN/tXwuCmO0/R1NKB50bZO3E2k1HdfR+p3aSjjt/3Fdn3jrolJt7WZTTbLEwldZK4RYUbvf7/cfWHHHRoTDlt2Jn2XXhn2ew+/I8k1ZNrPjbZf0eeY/EzFjJ+gcGX7OqtLFXF3xfUTWLqgl7K03Yf2nC/ksT9l+asP/ShP2XJuy//n1Cezs9KP2rgNUfMuvTnUFaWlpdVPnnjf9Eb5mUpHvr7/SW26Z/d1PiL/WWm4p/9UTQb3X/BhVNqAk1oSbsNSHLBn+n96SZ7C/1DkCtf0B/GXm/pZfa4fDvtH4Hoo68/6vSHl8TasL/V8J/3payo/ln+n70EMr/EFFH3lpaWlpaWlpaWlpaWlpaWlpaWlpaWlpa/1X9BxwfChGcLBSoAAAAAElFTkSuQmCC" alt="SDGs 15" style="width: 200px; margin: auto;">
            <p>SDGs 15</p>
        </div>
        """, unsafe_allow_html=True
    )

        with st.form("Blog_Form"):
            # Menambahkan CSS untuk styling
            st.markdown("""
            <style>
            .stButton { display: flex; justify-content: center; }
            .custom-title { font-size: 28px; font-weight: bold; } /* Mengubah ukuran font title */
            </style>
            """, unsafe_allow_html=True)

            def blog_post_with_image(title, img_path, description, link):
                st.markdown(f"<h3 style='text-align: center;'>{title}</h3>", unsafe_allow_html=True)
                st.image(img_path, caption=title, use_column_width=True)
                st.markdown(f"<p style='text-align: center;'>{description}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='text-align: center;'><a href='{link}' target='_blank'>Read More</a></p>", unsafe_allow_html=True)

            blog_data = [
                {
                    "title": "Pengertian Internet of Things",
                    "img_path": "Image/IoT.jpg",
                    "description": "Bagaimana teknologi IoT membuat pengelolaan bendungan lebih cerdas? Temukan jawabannya di sini.",
                    "link": "https://www.dicoding.com/blog/apa-itu-internet-of-things/"
                },
                {
                    "title": "Manfaat Energi Terbarukan PLTS",
                    "img_path": "Image/solar.jpg",
                    "description": "Apa saja manfaat dari PLTS? Cek di sini jawabannya",
                    "link": "https://sunenergy.id/blog/pembangkit-listrik-tenaga-surya"
                },
                {
                    "title": "Manfaat Energi Terbarukan PLTMH ",
                    "img_path": "Image/pltmh.jpg",
                    "description": "Berikut manfaat dari PLTMH",
                    "link": "https://myeco.id/manfaat-pembangkit-listrik-tenaga-mikro-hidro-pltmh/"
                },
                # Postingan tambahan
                {
                    "title": "4 Hydroponic Technologies in Japan",
                    "img_path": "Image/jepangHidroponik.jpg",
                    "description": "Discover the Latest Innovations in Hydroponics Transforming Farming in Japan! This article explores four advanced technologies being implemented in Japan.",
                    "link": "https://dlh.semarangkota.go.id/4-teknologi-hidroponik-di-jepang/"
                },
                {
                    "title": "Maximizing Hydroponic Lighting",
                    "img_path": "Image/tambahan.jpg",
                    "description": "Uncover the Secrets Behind Healthy Hydroponic Plant Growth! This article explores the essential requirements for hydroponic nutrition.",
                    "link": "https://www.kompasiana.com/madeyogi1918/60a34c648ede485a65284762/pencahayaan-tanaman-hidroponik-dalam-ruangan-guna-memaksimalkan-produktivitas-tanaman"
                },
                {
                    "title": "4 Tips for Maximizing Hydroponics",
                    "img_path": "Image/4tips.jpg",
                    "description": "Want a More Bountiful Hydroponic Harvest? Discover 4 Practical Tips to Optimize Hydroponic Plant Growth",
                    "link": "https://kebunpintar.id/blog/ketahui-4-tips-dalam-memaksimalkan-bercocok-tanam-metode-hidroponik/"
                }
            ]

            # Status untuk menentukan apakah lebih banyak postingan telah ditampilkan
            if 'more_posts' not in st.session_state:
                st.session_state.more_posts = False

            # Menampilkan blog dalam layout 3 kolom
            st.markdown("<h2 style='text-align: center;'>Latest Information on SERASI</h2>", unsafe_allow_html=True)
            st.markdown("<hr/>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)

            for i in range(3):
                with [col1, col2, col3][i]:
                    blog_post_with_image(**blog_data[i])

            # Mengatur tampilan tombol berdasarkan status more_posts
            if not st.session_state.more_posts:
                if st.form_submit_button("See More Posts"):
                    st.session_state.more_posts = True
            else:
                col4, col5, col6 = st.columns(3)
                for i in range(3, len(blog_data)):
                    with [col4, col5, col6][i - 3]:
                        blog_post_with_image(**blog_data[i])

                if st.form_submit_button("See Fewer Posts"):
                    st.session_state.more_posts = False

    # Monitoring section - Optimized
    elif menu_selection == "Monitoring":
        st.markdown("""
        <h1 style='text-align: center; margin: 0 auto; padding: 10px;'>Monitoring</h1>
        <style>
            h1 {
                text-align: center;
                margin: 0 auto; /* Pusatkan elemen */
                padding: 10px; /* Jarak internal untuk kenyamanan visual */
                font-size: 24px; /* Ukuran font menyesuaikan layar kecil */
            }
        </style>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        col6, col7, col8, col9, col10 = st.columns(5)
        
        # Display sensors in two rows
        sensors = [
            ("TDS Value", sensor_data['tds'], "ppm"),
            ("pH Value", sensor_data['ph'], ""),
            ("Water Temperature", sensor_data['water_temperature'], "°C"),
            ("Turbidity", sensor_data['turbidity'], "NTU"),
            ("Water Flow Rate", sensor_data['water_flow'], "L/min"),
            ("Distance", sensor_data['distance'], "cm"),
            ("Water Quality", sensor_data['water_quality'], ""),
            ("Voltage", sensor_data['tegangan'], "V"),
        ]
        columns = [col1, col2, col3, col4, col5, col7, col8, col9]
        for idx, (title, value, unit) in enumerate(sensors):
            with columns[idx]:
                st.markdown(f"""
                <div class="sensor-box">
                    <div class="sensor-title">{title}</div>
                    <div class="sensor-value">{value} {unit}</div>
                </div>
                """, unsafe_allow_html=True)


    elif menu_selection == "About Us":
        st.markdown("<h2 style='text-align: center;'>HYDRATS TEAM</h2>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns([0.1, 0.1, 0.1,0.1])

        # Menampilkan gambar di kolom dengan ukuran tertentu
        with col1: 
            img1 = Image.open('./Image/rega.png')
            st.image(img1, caption="Rega Arzula Akbar", use_column_width=True, width=30)
            st.markdown("""
            <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 20px; margin-top: 20px;">
           <div class="inovasi-box">
                <div class="inovasi-title">Rega Arzula Akbar</div>
                    <div class="inovasi-value">
                    S1 Teknik Elektro 
                    </div>
                </div>
            </div>
            <style>
    .inovasi-box {
        background-color: #f2f2f2; /* Warna abu-abu terang */
        border-radius: 12px; /* Membuat sudut lebih membulat */
        padding: 30px; /* Jarak dalam */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Efek bayangan lembut */
        text-align: center; /* Pusatkan teks */
        font-size: 14px; /* Ukuran font */
        margin: 50px; /* Jarak antar elemen */
        width: calc(100% - 40px); /* Default untuk layar kecil */
        max-width: 300px; /* Batas maksimum lebar */
    }
    .inovasi-title {
        font-size: 1.2em;
        color: black; /* Warna hitam untuk judul */
        font-weight: bold;
    }
    .inovasi-value {
        font-size: 1em;
        color: black; /* Warna hitam untuk teks */
        font-weight: normal;
    }
    .inovasi-box:hover {
        transform: scale(1.05); /* Sedikit memperbesar ukuran */
        transition: transform 0.2s ease-in-out; /* Efek transisi halus */
        background-color: #e0e0e0; /* Warna abu-abu sedikit lebih gelap saat hover */
    }
    </style>
            """, unsafe_allow_html=True)
        with col2:
            img2 = Image.open('./Image/rega.png')
            st.image(img2, caption="Rega Arzula Akbar", use_column_width=True, width=30)
            st.markdown("""
            <div class="inovasi-box">
            <div class="inovasi-title">Rega Arzula Akbar</div>
            <div class="inovasi-value">
                S1 Teknik Elektro 
            </div>
        </div>
        </div>
        <style>
    .inovasi-box {
        background-color: #f2f2f2; /* Warna abu-abu terang */
        border-radius: 12px; /* Membuat sudut lebih membulat */
        padding: 30px; /* Jarak dalam */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Efek bayangan lembut */
        text-align: center; /* Pusatkan teks */
        font-size: 14px; /* Ukuran font */
        margin: 50px; /* Jarak antar elemen */
        width: calc(100% - 40px); /* Default untuk layar kecil */
        max-width: 300px; /* Batas maksimum lebar */
    }
    .inovasi-title {
        font-size: 1.2em;
        color: black; /* Warna hitam untuk judul */
        font-weight: bold;
    }
    .inovasi-value {
        font-size: 1em;
        color: black; /* Warna hitam untuk teks */
        font-weight: normal;
    }
    .inovasi-box:hover {
        transform: scale(1.05); /* Sedikit memperbesar ukuran */
        transition: transform 0.2s ease-in-out; /* Efek transisi halus */
        background-color: #e0e0e0; /* Warna abu-abu sedikit lebih gelap saat hover */
    }
    </style>
        """, unsafe_allow_html=True)
        with col3:
            img3 = Image.open('./Image/miftah.png')
            st.image(img3, caption="Miftah Faqih", use_column_width=True, width=30)
            st.markdown("""
             <div class="inovasi-box">
            <div class="inovasi-title">Miftah Faqih</div>
            <div class="inovasi-value">
                S1 Teknik Elektro 
            </div>
            </div>
        </div> 
        <style>
    .inovasi-box {
        background-color: #f2f2f2; /* Warna abu-abu terang */
        border-radius: 12px; /* Membuat sudut lebih membulat */
        padding: 30px; /* Jarak dalam */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Efek bayangan lembut */
        text-align: center; /* Pusatkan teks */
        font-size: 14px; /* Ukuran font */
        margin: 50px; /* Jarak antar elemen */
        width: calc(100% - 40px); /* Default untuk layar kecil */
        max-width: 300px; /* Batas maksimum lebar */
    }
    .inovasi-title {
        font-size: 1.2em;
        color: black; /* Warna hitam untuk judul */
        font-weight: bold;
    }
    .inovasi-value {
        font-size: 1em;
        color: black; /* Warna hitam untuk teks */
        font-weight: normal;
    }
    .inovasi-box:hover {
        transform: scale(1.05); /* Sedikit memperbesar ukuran */
        transition: transform 0.2s ease-in-out; /* Efek transisi halus */
        background-color: #e0e0e0; /* Warna abu-abu sedikit lebih gelap saat hover */
    }
    </style>
        """, unsafe_allow_html=True)
        with col4:
            img4 = Image.open('./Image/brian.png')
            st.image(img4, caption="Bryan Sasabone", use_column_width=True, width=30)
            st.markdown("""
             <div class="inovasi-box">
            <div class="inovasi-title">Bryan Sasabone</div>
            <div class="inovasi-value">
                S1 Teknik Elektro 
            </div>
        </div>
    </div>
    <style>
    .inovasi-box {
        background-color: #f2f2f2; /* Warna abu-abu terang */
        border-radius: 12px; /* Membuat sudut lebih membulat */
        padding: 30px; /* Jarak dalam */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15); /* Efek bayangan lembut */
        text-align: center; /* Pusatkan teks */
        font-size: 14px; /* Ukuran font */
        margin: 50px; /* Jarak antar elemen */
        width: calc(100% - 40px); /* Default untuk layar kecil */
        max-width: 300px; /* Batas maksimum lebar */
    }
    .inovasi-title {
        font-size: 1.2em;
        color: black; /* Warna hitam untuk judul */
        font-weight: bold;
    }
    .inovasi-value {
        font-size: 1em;
        color: black; /* Warna hitam untuk teks */
        font-weight: normal;
    }
    .inovasi-box:hover {
        transform: scale(1.05); /* Sedikit memperbesar ukuran */
        transition: transform 0.2s ease-in-out; /* Efek transisi halus */
        background-color: #e0e0e0; /* Warna abu-abu sedikit lebih gelap saat hover */
    }
    </style>
    """, unsafe_allow_html=True)


    elif menu_selection == "FAQ":
        st.markdown("---", unsafe_allow_html=True)

        st.markdown("<h2 style='text-align: center;'>FAQ - SERASI System Features</h2>", unsafe_allow_html=True)

        st.markdown("### Frequently Asked Questions")
        
        with st.expander(" Apa tujuan utama dari sistem SERASI?"):
            st.write("""
            Tujuan utama SERASI adalah untuk menyediakan solusi teknologi berbasis Internet of Things (IoT) yang mendukung keberlanjutan pengelolaan air, energi, dan ekosistem. 
            Sistem ini dirancang untuk memantau, mengontrol, dan meningkatkan efisiensi pengelolaan bendungan di Kampung Pasir Honje.


            """)
        
        with st.expander("Bagaimana cara kerja sistem monitoring real-time pada SERASI?"):
            st.write("""
            Sistem monitoring menggunakan sensor IoT untuk mengumpulkan data seperti suhu, pH air, kualitas air, dan ketinggian air. 
            Data ini dikirim secara real-time ke dashboard, sehingga pengguna dapat memantau kondisi bendungan dari mana saja dan kapan saja.
            """)

        with st.expander("Apa saja teknologi yang digunakan dalam proyek ini?"):
            st.write("""
            1. IoT (Internet of Things): Untuk memantau data lingkungan.
            2. PLTS (Pembangkit Listrik Tenaga Surya): Menghasilkan energi terbarukan untuk mendukung operasional sistem.
            3. PLTMH (Pembangkit Listrik Tenaga Mikrohidro): Menggunakan aliran air untuk menghasilkan listrik.
            4. Website Interface yang interaktif
            """)
            
        with st.expander("Apa dampak positif dari implementasi proyek ini bagi masyarakat?"):
            st.write("""
            Dampak positif meliputi:
            - Penyediaan data real-time untuk mendukung keputusan pengelolaan bendungan.
            - Mengurangi ketergantungan pada sumber energi tidak terbarukan melalui PLTS dan PLTMH.
            - Meningkatkan produktivitas pertanian melalui pengelolaan air yang lebih baik.
            - Menjaga keseimbangan ekosistem sekitar bendungan.
            """)
            
        with st.expander("Bagaimana SERASI mendukung SDGs?"):
            st.write("""
            Proyek SERASI mendukung SDGs sebagai berikut:
            - SDGs 6: Meningkatkan akses air bersih dan sanitasi.
            - SDGs 7: Menggunakan energi terbarukan untuk mendukung pengelolaan sistem.
            - SDGs 15: Melindungi dan memulihkan ekosistem daratan di sekitar bendungan.
            """)

        with st.expander("Bagaimana cara masyarakat berkontribusi dalam proyek ini?"):
            st.write("""
            Masyarakat dapat berkontribusi dengan:
            - Memberikan data atau informasi terkait kondisi lingkungan.
            - Mengikuti pelatihan penggunaan sistem.
            - Membantu menjaga dan memelihara perangkat yang dipasang di lokasi.
            """)

        with st.expander("Apa kelebihan sistem SERASI dibandingkan dengan metode tradisional?"):
            st.write("""
            Sistem SERASI memiliki beberapa kelebihan:
            - Pemantauan dan kontrol otomatis berbasis teknologi.
            - Energi mandiri melalui pembangkit terbarukan.
            - Efisiensi dalam penggunaan air dan energi.
            - Pengurangan risiko kerusakan ekosistem melalui deteksi dini.
            """)
        

# Jalankan aplikasi Streamlit
if __name__ == '__main__':
    main()
