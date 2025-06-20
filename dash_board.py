from tkinter import *
from PIL import Image, ImageTk
import subprocess
import os
import pandas as pd

class Return_Period:
    def __init__(self, root, district=None):
        self.root = root
        self.district = district
        self.root.title("Return Rainfall Periods in Sri Lanka")
        self.root.geometry("1920x1000+0+0")

        bg_image = Image.open("background.jpg")
        bg_image = bg_image.resize((1920, 1000), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(bg_image)

        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        if not district:
            label = Label(self.root, text="SELECT DISTRICT:", font=("Algerian", 30, "bold"), bg="#FFFFFF", fg="#051626")
            label.place(relx=0.5, rely=0.10, anchor="center")

            self.district_var = StringVar()
            self.district_var.set("Select District")

            districts = [
                "Ampara", "Anuradhapura", "Badulla", "Batticaloa", "Colombo", "Galle", "Gampaha", "Hambantota",
                "Jaffna", "Kalutara", "Kandy", "Kegalle", "Kilinochchi", "Kurunegala", "Mannar", "Matale", "Matara",
                "Monaragala", "Mullaitivu", "Nuwara Eliya", "Polonnaruwa", "Puttalam", "Ratnapura", "Trincomalee", "Vavuniya"
            ]

            district_dropdown = OptionMenu(self.root, self.district_var, *districts, command=self.open_district_page)
            district_dropdown.config(font=("Helvetica", 18), width=60, bg="white", fg="black")
            district_dropdown.place(relx=0.5, rely=0.30, anchor="center")

        # else:
        #     label = Label(self.root, text=f"Rainfall Return Periods - {district.upper()}",
        #                   font=("Algerian", 30, "bold"), bg="#FFFFFF", fg="#051626")
        #     label.place(relx=0.5, rely=0.20, anchor="center")

        #     self.choice_var = StringVar()
        #     self.choice_var.set("Select Station")

        #     specific_files = [
        #         "CSV_ALUPOLA.csv", "CSV_CARNEY ESTATE.csv", "CSV_CHANDRIKAWEWA.csv", "CSV_DEPEDENA GROUP.csv",
        #         "CSV_DETANAGALLA.csv", "CSV_EHELIYAGODA S.P..csv", "CSV_EMBILIPITIYA.csv", "CSV_GALATURA ESTATE.csv",
        #         "CSV_GILIMALAY ESTATE.csv", "CSV_GODAKAWELA.csv", "CSV_HALLAYEN ESTATE.csv", "CSV_MUTWAGALLA ESTATE.csv",
        #         "CSV_non pariel.csv", "CSV_RASSAGALA.csv"
        #     ]

        #     station_names = [file.replace(".csv", "").replace("_", " ").title() for file in specific_files]

        #     if not station_names:
        #         Label(self.root, text="No station CSV files found for this district.",
        #               font=("Helvetica", 16), bg="#FFFFFF", fg="red").place(relx=0.5, rely=0.5, anchor="center")
        #     else:
        #         dropdown = OptionMenu(self.root, self.choice_var, *station_names)
        #         dropdown.config(font=("Helvetica", 16), width=60, bg="white", fg="black")
        #         dropdown.place(relx=0.5, rely=0.30, anchor="center")

        else:
            # District selected — show analysis options
            label = Label(self.root, text=f"Rainfall Return Periods - {district.upper()}",
                          font=("Algerian", 30, "bold"), bg="#FFFFFF", fg="#051626")
            label.place(relx=0.5, rely=0.20, anchor="center")

            self.choice_var = StringVar()
            self.choice_var.set("Select Analysis")

            analysis_choices = self.get_analysis_choices_for_district(district)

            if not analysis_choices:
                Label(self.root, text="No analysis files found for this district.",
                      font=("Helvetica", 16), bg="#FFFFFF", fg="red").place(relx=0.5, rely=0.5, anchor="center")
            else:
                dropdown = OptionMenu(self.root, self.choice_var, *analysis_choices.keys(),
                                      command=lambda choice: self.open_script(choice, analysis_choices))
                dropdown.config(font=("Helvetica", 16), width=60, bg="white", fg="black")
                dropdown.place(relx=0.5, rely=0.30, anchor="center")    

            self.add_generic_buttons(district)

            Button(self.root, text="Back", font=("Helvetica", 14, "bold"),
                   bg="#301934", fg="white", padx=20, pady=10,
                   command=self.go_back).place(relx=0.95, rely=0.95, anchor="se")

            Button(self.root, text="Find", font=("Helvetica", 14, "bold"),
                   bg="#301934", fg="white", padx=20, pady=10,
                   command=self.open_find_window).place(relx=0.05, rely=0.95, anchor="sw")

    # def get_analysis_choices_for_district(self, district_name):
    #     folder_path = os.path.join(os.getcwd(), district_name)
    #     if not os.path.exists(folder_path):
    #         print(f"Folder for district '{district_name}' not found.")
    #         return {}

    #     analysis_choices = {}
    #     for filename in os.listdir(folder_path):
    #         if filename.endswith(".py"):
    #             display_name = filename.replace(".py", "").replace("_", " ").title()
    #             analysis_choices[display_name] = os.path.join(folder_path, filename)

    #     return analysis_choices

    def get_analysis_choices_for_district(self, district_name):
        folder_path = os.path.join(os.getcwd(), district_name)
        if not os.path.exists(folder_path):
            print(f"Folder for district '{district_name}' not found.")
            return {}

        # ✅ Define allowed CSV files per district manually
        allowed_stations_by_district = {
            "Ratnapura": {
                "Alupola": "alupola.py",
                "Carney State": "carneystate.py",
                "Depadena": "Depedena.py",
                "Detanagalla": "Depedena.py",
                "Eheliyagoda": "eheliyagoda.py",
                "Embilipitiya": "embilipitiya.py",
                "Galatura": "galatuura.py",
                "Gilimalay": "gilimalay.py",
                "Godakawela": "godakawela.py",
                "Hallayen": "hallayen.py",
                "Mutwagalla": "mutwagalla.py",
                "Non Pariel": "pariel.py"
            },
            "Badulla": {
                "Badulla": "badulla.py",
                "Bandarawela": "bandarawela.py"
                # Add more as needed
            },
            "Colombo": {
                "Colombo Central": "colombo.py",
                "ratmalana": "ratmalana.py"
                
                # Add more as needed
            },
            # 🔄 Add more districts and their allowed station files here
        }

        # 📦 Get station list for the selected district
        station_dict = allowed_stations_by_district.get(district_name, {})

        analysis_choices = {}

        for station_name, filename in station_dict.items():
            full_path = os.path.join(folder_path, filename)
            if os.path.exists(full_path):  # Only add if CSV file exists
                display_name = f"Analyze Station - {station_name}"
                analysis_choices[display_name] = full_path

        return analysis_choices




    def open_script(self, choice, choices_dict):
        script_path = choices_dict.get(choice)
        if script_path:
            try:
                script_folder = os.path.dirname(script_path)
                script_name = os.path.basename(script_path)
                subprocess.Popen(["python", script_name], cwd=script_folder)
            except Exception as e:
                print(f"Error running {script_path}: {e}")

    def open_district_page(self, district_name):
        self.root.destroy()
        root = Tk()
        Return_Period(root, district=district_name)
        root.mainloop()

    def go_back(self):
        self.root.destroy()
        root = Tk()
        Return_Period(root, district=None)
        root.mainloop()

    def open_find_window(self):
        #pass  # unchanged for brevity

        
        find_window = Toplevel(self.root)
        find_window.title("Find Rainfall by Station")
        find_window.geometry("1920x1000+0+0")

        bg_image = Image.open("background.jpg")
        bg_image = bg_image.resize((1920, 1000), Image.LANCZOS)
        bg = ImageTk.PhotoImage(bg_image)

        find_window.bg = bg
        bg_label = Label(find_window, image=bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        try:
           # df = pd.read_csv("Combined_Rainfall_All_Stations_ratnapura.csv" )
           # Read both CSV files
            df_ratnapura = pd.read_csv("Combined_Rainfall_All_Stations_ratnapura.csv")
            df_colombo = pd.read_csv("Combined_Rainfall_All_Stations_colombo.csv")
            df_badulla = pd.read_csv("Combined_Rainfall_All_Stations_badulla.csv")

            # Combine them into one DataFrame
            df = pd.concat([df_ratnapura, df_colombo, df_badulla], ignore_index=True)
            #print(df_combined.head())
            df.columns = df.columns.str.strip()
            df = df.rename(columns={"station_name": "Station", "obs": "Rainfall_mm", "Date": "Date"})

            stations = df['Station'].unique().tolist()

            Label(find_window, text="FIND RAINFALL DATA BY STATION", font=("Helvetica", 24, "bold"), bg="#FFFFFF").pack(pady=20)

            

            Label(find_window, text="Select Station:", font=("Helvetica", 16), bg="#FFFFFF").pack(pady=10)
            station_var = StringVar()
            station_var.set(stations[0])
            station_menu = OptionMenu(find_window, station_var, *stations)
            station_menu.config(font=("Helvetica", 14), width=30)
            station_menu.pack(pady=5)

            Label(find_window, text="Enter Rainfall Amount (mm):", font=("Helvetica", 16), bg="#FFFFFF").pack(pady=10)
            rainfall_entry = Entry(find_window, font=("Helvetica", 14))
            rainfall_entry.pack(pady=5)

            result_label = Label(find_window, text="Latest Date: ", font=("Helvetica", 16, "bold"), fg="blue", bg="#FFFFFF")
            result_label.pack(pady=20)

            def find_latest_date():
                try:
                    selected_station = station_var.get()
                    min_rainfall = float(rainfall_entry.get())
                    df_filtered = df[(df['Station'] == selected_station) & (df['Rainfall_mm'] >= min_rainfall)]

                    if not df_filtered.empty:
                        latest_date = df_filtered['Date'].max()
                        result_label.config(text=f"Latest Date: {latest_date}")
                    else:
                        result_label.config(text="No data found")
                except Exception as e:
                    result_label.config(text=f"Error: {e}")

            Button(find_window, text="Find", font=("Helvetica", 14, "bold"),
                   bg="#301934", fg="white", padx=20, pady=10,
                   command=find_latest_date).pack(pady=10)

        except Exception as e:
            Label(find_window, text=f"Error loading CSV: {e}", font=("Helvetica", 14), fg="red", bg="#FFFFFF").pack(pady=40)

        Button(find_window, text="Close", font=("Helvetica", 14),
               command=find_window.destroy).place(relx=0.5, rely=0.95, anchor="s")

    def run_script(self, script_path):
        try:
            full_path = os.path.abspath(script_path)
            script_folder = os.path.dirname(full_path)
            script_name = os.path.basename(full_path)
            subprocess.Popen(["python", script_name], cwd=script_folder)
        except Exception as e:
            print(f"Error running {script_path}: {e}")


    def add_generic_buttons(self, district):
        base_path = os.path.join(district, district.lower())
        #base_path = os.path.join(district, f"{district}")


        Button(
            self.root,
            text="Plot Seasonal Return Period - Monthly Areal Data",
            font=("Helvetica", 14, "bold"), bg="#DFC5FE", fg="black", padx=20, pady=10,
            command=lambda: self.run_script(f"{base_path}_seasonal.py")
        ).place(relx=0.5, rely=0.40, anchor="center")

        Button(
            self.root,
            text="Plot Seasonal Return Period - Daily Data",
            font=("Helvetica", 14, "bold"), bg="#DFC5FE", fg="black", padx=20, pady=10,
            command=lambda: self.run_script(f"{base_path}_season_daily.py")
        ).place(relx=0.5, rely=0.50, anchor="center")

        Button(
            self.root,
            text="District Graph - Monthly Areal",
            font=("Helvetica", 14, "bold"), bg="#DFC5FE", fg="black", padx=20, pady=10,
            command=lambda: self.run_script(f"{base_path}_district.py")
        ).place(relx=0.5, rely=0.60, anchor="center")

        Button(
            self.root,
            text="District Graph - Daily",
            font=("Helvetica", 14, "bold"), bg="#DFC5FE", fg="black", padx=20, pady=10,
            command=lambda: self.run_script(f"{base_path}_district_withdailyrainfall.py")
        ).place(relx=0.5, rely=0.70, anchor="center")

        Button(
            self.root,
            text="All Station Return Rainfall",
            font=("Helvetica", 14, "bold"), bg="#DFC5FE", fg="black", padx=10, pady=5,
            command=lambda: self.run_script(f"{base_path}_all_in_one.py")
        ).place(relx=0.5, rely=0.80, anchor="center")

if __name__ == "__main__":
    root = Tk()
    app = Return_Period(root)
    root.mainloop()
