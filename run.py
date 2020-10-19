from Pi_Epaper import PiCalendar

def main():
    # Use your own iCloud/Google/icals calendar subscription/share link here!
    url = ""
    delgate = PiCalendar(url=url)
    delgate.update()

if __name__ == '__main__':
	main()
