import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_NAMES = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
SHORT_MONTH_NAMES = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
DAY_NAMES = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington)
    city = get_city_filter_input()
    print('--> {city} is chosen.'.format(city = city.title()))

    # Get user input for month (all, january, february, ... , june)
    month = get_month_filter_input()
    if(month == 'all'):
        print('--> No month filter is chosen.')
    else:
        print('--> {month} is chosen.'.format(month = month.title()))

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day_of_week_filter_input()
    if(day == 'all'):
        print('--> No day filter is chosen.')
    else:
        print('--> {day} is chosen.'.format(day = day.title()))

    print('-'*40)
    return city, month, day

def get_city_filter_input():
    """
    Asks user to specify a city to analyze.
    User can chose between Chicago, New York and Washington. The input is case insensitive.

    Returns:
        (str) city - name of the city to analyze
    """
    while True:
        try:
            input_guide_str = '\nPlease select city to analyze:'
            input_guide_str += '\n1. Chicago'
            input_guide_str += '\n2. New York'
            input_guide_str += '\n3. Washington\n'
            user_input = input(input_guide_str).strip().lower()

            if user_input in ['1', 'chicago']:
                return 'chicago'
            elif user_input in ['2', 'new york city', 'new york', 'ny']: 
                return 'new york city'
            elif user_input in ['3', 'washington', 'wa']:
                return 'washington'
            else:
                print('\nInvalid City. Please try again.')
        except:
            print('\nInvalid City. Please try again.')

def get_month_filter_input():
    """
    Get user input for month.
    """
    while True:
        try:
            input_guide_str = '\nPlease type name of the month you want to filter by (type "all" or "none" to apply no month filter):\n'
            user_input = input(input_guide_str).strip().lower()

            if(user_input in ['all', 'none', 'no', '0']):
                return 'all'
            elif(user_input in MONTH_NAMES):
                return user_input
            elif(user_input in SHORT_MONTH_NAMES):
                return MONTH_NAMES[SHORT_MONTH_NAMES.index(user_input)]
            elif(int(user_input) >= 1 and int(user_input) <= 12):
                return MONTH_NAMES[int(user_input) - 1]
            else:
                print('\nInvalid Month. Please try again.')
        except:
            print('\nInvalid Month. Please try again.')

def get_day_of_week_filter_input():
    """
    Get user input for day of week.
    """
    short_day_names = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
    shorter_day_names = ['su', 'mo', 'tu', 'we', 'th', 'fr', 'sa']
    while True:
        try:
            input_guide_str = '\nPlease type the day of week you want to filter by (type "all" or "none" to apply no day filter):\n'
            user_input = input(input_guide_str).strip().lower()

            if(user_input in ['all', 'none', 'no', '0']):
                return 'all'
            elif(user_input in DAY_NAMES):
                return user_input
            elif(user_input in short_day_names):
                return DAY_NAMES[short_day_names.index(user_input)]
            elif(user_input in shorter_day_names):
                return DAY_NAMES[shorter_day_names.index(user_input)]
            elif(int(user_input) >= 1 and int(user_input) <= 7):
                return DAY_NAMES[int(user_input) - 1]
            else:
                print('\nInvalid Day of week. Please try again.')
        except:
            print('\nInvalid Day of week. Please try again.')

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
        df_raw - Pandas DataFrame containing city's raw data
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    df_raw = pd.DataFrame.copy(df)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    df = filter_by_month(df, month)

    # filter by day of week if applicable
    df = filter_by_day_of_week(df, day)

    return df, df_raw

def filter_by_month(df, month):
    """Filter by month depends on the month taken in."""
    try:
        if month == 'all':
            return df
        
        # use the index of the months list to get the corresponding int
        month_num = MONTH_NAMES.index(month) + 1

        # filter by month to create the new dataframe
        df_filtered = df[df['month'] == month_num]
        return df_filtered  
    
    except:
        return df

def filter_by_day_of_week(df, day):
    """Filter by day of week depends on the day of week taken in."""
    try:
        if day == 'all':
            return df
        
        # filter by day of week to create the new dataframe
        df_filtered = df[df['day_of_week'] == day.title()] 
        return df_filtered
    
    except:
        return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    top_month = df['month'].value_counts().head(1)
    name = convert_month_number_to_month_name(top_month.index[0]).title()
    count = top_month[top_month.index[0]]
    print('The month with most travel: {name} | Count: {count}'.format(name = name, count = count))

    # Display the most common day of week
    top_day = df['day_of_week'].value_counts().head(1)
    name = top_day.index[0]
    count = top_day[top_day.index[0]]
    print('\nThe day of week with most travel: {name} | Count: {count}'.format(name = name, count = count))

    # Display the most common start hour
    top_hour = df['Start Time'].dt.hour.value_counts().head(1)
    name = top_hour.index[0]
    count = top_hour[top_hour.index[0]]
    print('\nThe hour with most travel (start hour): {name} | Count: {count}'.format(name = name, count = count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_month_number_to_month_name(month_number):
    """Convert month number (1 -> 12) to month name"""
    if(month_number < 1 or month_number > 12):
        return ''
    return MONTH_NAMES[month_number - 1]

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    top_start_station = df['Start Station'].value_counts().head(1)
    name = top_start_station.index[0]
    count = top_start_station[top_start_station.index[0]]
    print('The most popular Start station:\n{name} | Count: {count}'.format(name = name, count = count))

    # Display most commonly used end station
    top_end_station = df['End Station'].value_counts().head(1)
    name = top_end_station.index[0]
    count = top_end_station[top_end_station.index[0]]
    print('\nThe most popular End station:\n{name} | Count: {count}'.format(name = name, count = count))

    # Display most frequent combination of start station and end station trip
    df['Station Combination'] = ' -> '
    df['Station Combination'] = df['Start Station'] + df['Station Combination'] + df['End Station']
    top_station_combination = df['Station Combination'].value_counts().head(1)
    name = top_station_combination.index[0]
    count = top_station_combination[top_station_combination.index[0]]
    print('\nThe most popular station combination:\n{name} | Count: {count}'.format(name = name, count = count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_seconds = df['Trip Duration'].sum()
    result_str = 'Total travel time: {seconds} seconds'.format(seconds = total_seconds)
    biggest_unit_string = convert_second_to_bigger_unit_for_display(total_seconds)
    if(biggest_unit_string != ''):
        result_str += ' = ' + biggest_unit_string
    print(result_str)

    # Display mean travel time
    means_seconds = df['Trip Duration'].mean()
    result_str = '\nAverage (mean) travel time: {seconds} seconds'.format(seconds = means_seconds)
    biggest_unit_string = convert_second_to_bigger_unit_for_display(means_seconds)
    if(biggest_unit_string != ''):
        result_str += ' = ' + biggest_unit_string
    print(result_str)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def convert_second_to_bigger_unit_for_display(seconds):
    """
    Conver the number of seconds to string of biggest unit possible (minute/hour) for displaying.
    If not possible to convert to bigger unit, returns empty string.
    """
    if(seconds/60/60 >= 1):
        return '{hours} hours'.format(hours = round(seconds/60/60, 2))
    elif(seconds/60 >= 1):
        return '{minutes} minutes'.format(minutes = round(seconds/60, 2))
    return ''

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print('Count of User types:')
    print(count_user_type.to_string())

    # Display counts of gender
    try:
        count_gender = df['Gender'].value_counts()
        print('\nCount of Genders:')
        print(count_gender.to_string())
    except:
        print('\nGender stats are unavailable.')

    # Display earliest, most recent, and most common year of birth
    try:
        years_of_birth = df['Birth Year'].dropna().astype('int')
        print('\nEarliest Year of birth: {year}'.format(year = years_of_birth.min()))
        print('\nMost recent Year of birth: {year}'.format(year = years_of_birth.max()))
        most_common_year = years_of_birth.value_counts().head(1)
        print('\nMost common Year of birth: {year}'.format(year = most_common_year.index[0]))
    except:
        print('\nBirth Year stats are unavailable.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_filter_statement(city, month, day):
    """Take in city, month and day of week filters, print a statement about filters on the results."""
    statement_str = '\n*All results are from data of {city}'.format(city = city.title())

    month_filter = False
    day_filter = False
    if(month not in ('all', '')):
       month_filter = True
    if(day not in ('all', '')):
       day_filter = True
    
    if(month_filter and day_filter):
        statement_str += ', filtered by both Month ({month}) and Day of Week ({day}).'.format(month = month.title(), day = day.title())
    elif(month_filter):
        statement_str += ', filtered by Month ({month}).'.format(month = month.title())
    elif(day_filter):
        statement_str += ', filtered by Day of Week ({day}).'.format(day = day.title())
    else:
        statement_str += '.'
    print(statement_str)

def display_raw_data(df):
    """Display raw day of the city by 5 rows each time the user confirms."""
    while True:
        display = input('\nWould you like to see 5 rows of raw data? (Enter yes or no)\n')
        if display.lower()  in ['no', 'n']:
            return
        elif display.lower() in ['yes', 'y']:
            start_index = 0
            end_index = 5
            if(end_index >= df.shape[0]):
                end_index = -1
            print(df.iloc[start_index:end_index])
            if(end_index == -1):
                return
            while(start_index < df.shape[0]):
                next = input('\nWould you like to see next 5 rows? (Enter yes or no)\n')
                if next.lower() in ['no', 'n']:
                    return
                elif next.lower() in ['yes', 'y']:
                    start_index += 5
                    end_index += 5
                    if(end_index >= df.shape[0]):
                        end_index = -1
                    print(df.iloc[start_index:end_index])
                    if(end_index == -1):
                        return
                else:
                    print('\nInvalid input. Please try again.')
        else:
            print('\nInvalid input. Please try again.')


def main():
    while True:
        city, month, day = get_filters()

        df, df_raw = load_data(city, month, day)
        
        if(df.shape[0] == 0):
            print('\nThere is no data for the selected filters.')
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            print_filter_statement(city, month, day)
            display_raw_data(df_raw)
        while True:
            restart = input('\nWould you like to restart? (Enter yes or no)\n')
            if restart.lower() in ['no', 'n']:
                return
            elif restart.lower() in ['yes', 'y']:
                print('\n\n')
                break
            else:
                print('\nInvalid input. Please try again.')


if __name__ == "__main__":
	main()
