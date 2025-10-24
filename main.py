import app_menu
import sys

if __name__ == "__main__":
    try:
        app = app_menu.App()
        app.mainloop()
    except KeyboardInterrupt:
        print("\nSaliendo de la aplicación.")
        sys.exit(0)
