
import sys

def get_estimated_time_of_work(check_time, check_pages, torah_pages):
    seconds_for_page = check_time // check_pages
    estimated_time   = seconds_for_page * torah_pages
    return estimated_time + 7 * 60

def to_hours(seconds):
    total_minutes = seconds // 60
    total_hours   = total_minutes // 60
    total_seconds = seconds % 60
    total_minutes = total_minutes % 60
    s = total_seconds
    m = total_minutes
    h = total_hours
    total_time = f'{h:02}:{m:02}:{s:02}'
    return total_time

def get_time_of_work(total_pages, seconds_for_page):
    total_seconds = total_pages * seconds_for_page
    total_minutes = total_seconds // 60
    total_seconds = total_seconds % 60
    total_hours = total_minutes // 60
    total_minutes = total_minutes % 60

    s = total_seconds
    m = total_minutes
    h = total_hours

    total_time = f'{h:02}:{m:02}:{s:02}'

    return total_time

def main():
    if len(sys.argv) >= 4:
        work_seconds = get_estimated_time_of_work(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    elif len(sys.argv) == 2 and sys.argv[1] == "--help":
        print("work_time_calc [check_time] [checked_pages] [torah_pages]")
        exit()
    else:
        check_time = input("Enter time of check (leave empty for 90 seconds):")
        if check_time == '':
            check_time = 90
        check_time = int(check_time)
        check_pages = int(input("Enter the number of pages were done in the check:"))
        torah_pages = int(input("Enter the number of pages in the torah scroll:"))
        work_seconds = get_estimated_time_of_work(check_time, check_pages, torah_pages)
    total_time = to_hours(work_seconds)
    print(f"Total time: {total_time}", end='')
    
if __name__ == '__main__':
    main()