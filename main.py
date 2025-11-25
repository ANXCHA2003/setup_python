import tkinter as tk
from tkinter import messagebox, simpledialog

DATA_FILE = "data.txt"


def save_data(name: str) -> None:
    with open(DATA_FILE, "a", encoding="utf-8") as file:
        file.write(name + "\n")


def open_add_window(root: tk.Tk) -> None:
    window = tk.Toplevel(root)
    window.title("เพิ่มข้อมูลชื่อ")
    window.geometry("500x500")

    tk.Label(window, text="กรุณาใส่ชื่อของคุณ:").pack(pady=10)
    name_entry = tk.Entry(window, width=30)
    name_entry.pack(pady=5)

    def on_save() -> None:
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("ข้อผิดพลาด", "กรุณาใส่ชื่อก่อนบันทึก!")
            return
        save_data(name)
        messagebox.showinfo("สำเร็จ", "บันทึกข้อมูลเรียบร้อยแล้ว!")
        window.destroy()

    tk.Button(window, text="บันทึกข้อมูล", command=on_save).pack(pady=10)


def show_data(root: tk.Tk) -> None:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = file.readlines()
    except FileNotFoundError:
        messagebox.showwarning("ข้อผิดพลาด", "ยังไม่มีข้อมูลบันทึก!")
        return

    window = tk.Toplevel(root)
    window.title("แสดงข้อมูลชื่อ")
    window.geometry("400x400")

    text_area = tk.Text(window, wrap=tk.WORD)
    text_area.pack(expand=True, fill=tk.BOTH)
    for line in data:
        text_area.insert(tk.END, line)


def manage_data(root: tk.Tk) -> None:
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = file.readlines()
    except FileNotFoundError:
        messagebox.showwarning("ข้อผิดพลาด", "ยังไม่มีข้อมูลบันทึก!")
        return

    window = tk.Toplevel(root)
    window.title("จัดการข้อมูลชื่อ")
    window.geometry("500x500")

    listbox = tk.Listbox(window)
    listbox.pack(expand=True, fill=tk.BOTH)
    for line in data:
        listbox.insert(tk.END, line.strip())

    def delete_selected() -> None:
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("ข้อผิดพลาด", "กรุณาเลือกข้อมูลที่จะลบ!")
            return
        index = selected[0]
        listbox.delete(index)
        data.pop(index)
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            file.writelines(data)
        messagebox.showinfo("สำเร็จ", "ลบข้อมูลเรียบร้อยแล้ว!")

    def edit_selected() -> None:
        selected = listbox.curselection()
        if not selected:
            messagebox.showwarning("ข้อผิดพลาด", "กรุณาเลือกข้อมูลที่จะแก้ไข!")
            return
        index = selected[0]
        current_value = data[index].strip()
        new_value = simpledialog.askstring(
            "แก้ไขข้อมูล", "ปรับชื่อเป็น:", initialvalue=current_value, parent=window
        )
        if new_value is None:
            return  # ผู้ใช้กด Cancel
        new_value = new_value.strip()
        if not new_value:
            messagebox.showwarning("ข้อผิดพลาด", "ค่าที่แก้ไขต้องไม่ว่างเปล่า!")
            return

        data[index] = new_value + "\n"
        listbox.delete(index)
        listbox.insert(index, new_value)
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            file.writelines(data)
        messagebox.showinfo("สำเร็จ", "แก้ไขข้อมูลเรียบร้อยแล้ว!")

    btn_frame = tk.Frame(window, pady=10)
    btn_frame.pack()
    tk.Button(btn_frame, text="แก้ไขข้อมูลที่เลือก", width=20, command=edit_selected).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="ลบข้อมูลที่เลือก", width=20, command=delete_selected).pack(side=tk.LEFT, padx=5)


def main() -> None:
    root = tk.Tk()
    root.title("โปรแกรมจัดการข้อมูลชื่อ")
    root.geometry("500x500")

    # ปุ่มลัดบนหน้าหลัก (macOS จะเห็นเมนูด้านบนจอ ทำให้หลายคนหาเมนูไม่เจอ)
    button_frame = tk.Frame(root, pady=40)
    button_frame.pack()
    tk.Button(button_frame, text="เพิ่มข้อมูล", width=20, command=lambda: open_add_window(root)).pack(pady=5)
    tk.Button(button_frame, text="แสดงข้อมูล", width=20, command=lambda: show_data(root)).pack(pady=5)
    tk.Button(button_frame, text="แก้ไข/ลบข้อมูล", width=20, command=lambda: manage_data(root)).pack(pady=5)
    tk.Button(button_frame, text="ออกจากโปรแกรม", width=20, command=root.destroy).pack(pady=5)

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    main_menu = tk.Menu(menu_bar, tearoff=0)
    main_menu.add_command(label="เพิ่มข้อมูล", command=lambda: open_add_window(root))
    main_menu.add_command(label="แสดงข้อมูล", command=lambda: show_data(root))
    main_menu.add_command(label="แก้ไข/ลบข้อมูล", command=lambda: manage_data(root))
    main_menu.add_separator()
    main_menu.add_command(label="ออกจากโปรแกรม", command=root.destroy)
    menu_bar.add_cascade(label="เมนูหลัก", menu=main_menu)

    root.mainloop()


if __name__ == "__main__":
    main()
