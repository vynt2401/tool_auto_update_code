import customtkinter as ctk
import socket
import requests
import dns.resolver

class ip():
    def __init__(self):
        self.local_ip = self.get_local_ip()
        self.public_ip = self.get_public_ip()
        self.dns_names = self.lookup_dns(self.public_ip)
        self.geolocation_info = self.get_ip_geolocation(self.public_ip)
    

    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))

            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception as e:
            return f"can't take local ip: {e}"

    def get_public_ip(self):
        try:
            response = requests.get("https://api.ipify.org?format=json")
            response.raise_for_status()
            return response.json()["ip"]
        except requests.exceptions.RequestException as e:
            return f"can't take public ip: {e}"
        
    def lookup_dns(self, ip_address):
        try:
            reversed_ip = '.'.join(ip_address.split('.')[::-1]) + '.in-addr.arpa'
            answers = dns.resolver.resolve(reversed_ip, 'PTR')
            dns_names = [str(rdata) for rdata in answers]
            return dns_names
        except dns.resolver.NXDOMAIN:
            return ["Can't find domain name (NXDOMAIN)"]
        except dns.resolver.NoAnswer:
            return ["Not have record PTR (NoAnswer)"]
        except dns.resolver.Timeout:
            return ["Over time to take DNS"]
        except Exception as e:
            return [f"ERROR with DNS: {e}"]

    def get_ip_geolocation(self, ip_address):
        try:
            response = requests.get(f"https://ipapi.co/{ip_address}/json/")
            response.raise_for_status()
            data = response.json()
            if data.get("error"):
                return f"Error from geolocation API: {data['reason']}"

            city = data.get("city", "Unknown")
            region = data.get("region", "Unknown")
            country_name = data.get("country_name", "Unknown")
            latitude = data.get("latitude", "Unknown")
            longitude = data.get("longitude", "Unknown")
            org = data.get("org", "Unknown")

            return {
                "city": city,
                "region": region,
                "country_name": country_name,
                "latitude": latitude,
                "longitude": longitude,
                "org": org
            }
        except requests.exceptions.RequestException as e:
            return f"Error with geolocation API: {e}"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("IP and dns app")
        self.geometry("300x400")

     
        self.label = ctk.CTkLabel(self, text="Testing...\n")
        self.label.pack(pady=20)

        info_text = f"Local IP: {ip().local_ip}\n" \
                    f"Public IP: {ip().public_ip}\n" \
                    f"DNS Names: {', '.join(ip().dns_names)}\n" \
                    f"Geolocation Info:\n" 
        
        self.info_box = ctk.CTkTextbox(self, width=400, height=200)
        self.info_box.pack(pady=20, padx=20, fill='both', expand=True)
        self.info_box.insert("0.0", info_text)
        self.info_box.configure(state="disabled")  # Make the textbox read-only



        self.button = ctk.CTkButton(self, text = "ip to website", command=self.on_button_click)
        self.button.pack(pady=20, padx=20)


    def on_button_click(self):
        input_window = ctk.CTkToplevel(self)
        input_window.title("Input name website")
        input_window.geometry("500x200")

        label = ctk.CTkLabel(input_window, text="Enter name of website:")
        label.pack(pady=20, padx=20)

        entry = ctk.CTkEntry(input_window, placeholder_text="Enter website name, e.g: example.com")
        entry.pack(pady=10, padx=20, fill='x', expand=True)


        def submit():
            text = entry.get()
            print(f"You entered: {text}")
            dns_record = {}
            a_record = dns.resolver.resolve(text, 'A') 
            for ipval in a_record:
                dns_record['A_Record_IP'] = ipval.to_text()
            mx_record_list = []
            mx_record = dns.resolver.resolve(text, 'MX')
            for server in mx_record:
                mx_record_list.append(server)
            for i, element in enumerate(mx_record_list):
                dns_record[f'MX_Record_{i+1}'] = element.to_text()  
            for key, value in dns_record.items():
                print(f"{key}={value}")

            

            input_window.destroy()

        submit_button = ctk.CTkButton(input_window, text="Submit", command=submit)
        submit_button.pack(pady=10, padx=20)



print("Starting the app...")



app = App()
app.mainloop()