import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

FILTER_CHOICES = ('month', 'day', 'both', 'none')

CITY_MONTHS = ('january', 'febuary', 'march', 'april', 'may', 'june')
#   'july', 'august', 'september', 'october', 'november', 'december'

CITY_DAYS = ('sunday', 'monday', 'tuesday', 'wednesday',
             'thursday', 'friday', 'saturday')


def get_city():
    '''Ask the person to specify a city to analyze.

    Returns:
        (str) city - name of the city to analyze
    '''

    city_names = list(CITY_DATA.keys())
    city_names.append('all')
    city = ''

    while ((city not in city_names) and (city != 'quit')):
        city = input('\nChoose a city ({}), type all for all cities or type '
                     'Quit to exit:'
                     ' '.format(', '.join(city_names).title())).lower()

    return city


def load_city(city):
    '''Load data for the specified city.

    Args:
        (str) city - name of the city to analyze
    Returns:
        (dataframe)df - Pandas DataFrame containing city data
    '''

    if city == 'all':
        df_from_each_file = []
        for key, value in CITY_DATA.items():
            print('Loading {} data...'.format(key.title()))
            df_from_file = pd.read_csv(CITY_DATA[key], parse_dates=[
                'Start Time', 'End Time'])
            df_from_file['City'] = key.title()
            df_from_each_file.append(df_from_file)

        df = pd.concat(df_from_each_file, ignore_index=True, sort=False)
    else:
        print('Loading {} data...'.format(city.title()))
        df = pd.read_csv(CITY_DATA[city], parse_dates=[
                         'Start Time', 'End Time'])

    pd.set_option('max_colwidth', 100)
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['trip'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')

    return df


def get_filter():
    '''Ask the person to specify a filter type for the data.

    Args:
        none
    Returns:
        (str) filter for the data
    '''
    choice = ''

    while ((choice not in FILTER_CHOICES)
           and (choice != 'quit')):
        choice = input('Choose how to filter ({}) or type Quit to exit:'
                       ' '.format(', '.join(FILTER_CHOICES).title())).lower()

    return choice


def get_month():
    '''Ask the person to specify a month to analyze.

    Args:
        none
    Returns:
        (str) month - name of the month to filter by
    '''
    month = ''

    while ((month not in CITY_MONTHS) and (month != 'quit')):
        month_choice = input('Choose a month by name ({}) or number '
                             '(1 = January) or type Quit to exit:'
                             ' '.format(', '.join(CITY_MONTHS).title()))

        if month_choice.isdigit() is True:
            if int(month_choice) < (len(CITY_MONTHS) + 1):
                month = CITY_MONTHS[int(month_choice) - 1].lower()
        else:
            month = month_choice.lower()

    return month


def filter_by_month(df, month):
    '''Filter the data by the chosen month.

    Args:
        (dataframe)df - Pandas DataFrame to filter
        (str) month - name of the month to filter by
    Returns:
        (str) df - Pandas DataFrame containing filtered data
    '''

    print('Filtering by {} month...'.format(month.title()))

    month_index = CITY_MONTHS.index(month.lower()) + 1
    filter_start = '2017-{}'.format(month_index)
    filter_end = '2017-{}'.format(month_index + 1)

    df_filtered = df[(df['Start Time'] >= filter_start) &
                     (df['Start Time'] < filter_end)]

    return df_filtered


def get_day():
    '''Ask the person to specify a day to analyze.

    Args:
        none
    Returns:
        (str) day - name of the day of week to filter by
    '''
    day = ''

    while ((day not in CITY_DAYS) and (day != 'quit')):
        day_choice = input('Choose a day of the week by name ({}) or number '
                           '(1 = Sunday) or type Quit to exit:'
                           ' '.format(', '.join(CITY_DAYS).title()))

        if day_choice.isdigit() is True:
            if int(day_choice) < (len(CITY_DAYS) + 1):
                day = CITY_DAYS[int(day_choice) - 1].lower()
        else:
            day = day_choice.lower()

    return day


def filter_by_day(df, day):
    '''Filter the data by the chosen day of the week

    Args:
        (dataframe)df - Pandas DataFrame to filter
        (str) day - name of the day of the week to filter by
    Returns:
        (dataframe) df - Pandas DataFrame containing filtered data
    '''

    print('Filtering by {}...'.format(day.title()))
    # day_name  # weekday_name
    # dayofweek
    df_filtered = df[df['day_of_week'] == day.title()]

    return df_filtered


def time_stats(df):
    '''Displays the statistics on the most frequent times of travel.

    Args:
        (dataframe)df - Pandas DataFrame to show time statistics
    Returns:
        none
    '''

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    index = int(df['Start Time'].dt.month.mode())
    common_month = CITY_MONTHS[index - 1]
    print('The common month is {}.'.format(common_month))

    # TO DO: display the most common day of week
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
    index = int(df['Start Time'].dt.dayofweek.mode())
    common_day_of_week = days_of_week[index]
    print("The common day of Week: {}.".format(common_day_of_week))

    # TO DO: display the most common start hour
    am_pm = 'am'
    common_hour = int(df['Start Time'].dt.hour.mode())
    if common_hour == 0:
        common_hour = 12
    elif 1 <= common_hour < 13:
        common_hour = common_hour
    elif 13 <= common_hour < 24:
        am_pm = 'pm'
        common_hour = common_hour - 12
    print('The common hour {}{}.'.format(common_hour, am_pm))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    '''Displays the statistics on the most popular stations and trip.

    Args:
        (dataframe)df - Pandas DataFrame to show station statistics
    Returns:
        none
    '''

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start = df['Start Station'].mode().to_string(index=False)
    print('The common start station is {}.'.format(common_start))

    # TO DO: display most commonly used end station
    common_end = df['End Station'].mode().to_string(index=False)
    print('The common end station is {}.'.format(common_end))

    # TO DO: display most frequent combination of start station and
    #        end station trip
    common_trip = df['trip'].mode().to_string(index=False)
    print('The common trip is {}.'.format(common_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    '''Displays the statistics on the total and average trip duration.

    Args:
        (dataframe)df - Pandas DataFrame to show trip durations
    Returns:
        none
    '''

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_trip_duration = df['Trip Duration'].sum()
    total_trip_duration_minute, total_trip_duration_second = divmod(
        total_trip_duration, 60)
    total_trip_duration_hour, total_trip_duration_minute = divmod(
        total_trip_duration_minute, 60)
    print('The total trip duration is {:,} hours, {} minutes and {} seconds'
          '.'.format(total_trip_duration_hour, total_trip_duration_minute,
                     total_trip_duration_second))

    # TO DO: display mean travel time
    average_trip_duration = round(df['Trip Duration'].mean())
    average_trip_duration_minute, average_trip_duration_second = divmod(
        average_trip_duration, 60)
    if average_trip_duration_minute > 60:
        average_trip_duration_hour, average_trip_duration_minute = divmod(
            average_trip_duration_minute, 60)
        print('The average trip duration is {} hours, {} minutes and {}'
              ' seconds.'.format(average_trip_duration_hour,
                                 average_trip_duration_minute,
                                 average_trip_duration_second))
    else:
        print('The average trip duration is {} minutes and {} seconds.'.format(
            average_trip_duration_minute, average_trip_duration_second))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    '''Displays the statistics about the people.

    Args:
        (dataframe)df - Pandas DataFrame to show individual statistics
    Returns:
        none
    '''

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # subs = df.query('"User Type" == "Subscriber"').user_type.count()
    subscribers = df[df['User Type'] == "Subscriber"].shape[0]
    # cust = df.query('"User Type" == "Customer"').user_type.count()
    customers = df[df['User Type'] == "Customer"].shape[0]
    print('There are {:,} Subscribers.\nThere are {:,} Customers.'.format(
        subscribers, customers))

    # TO DO: Display counts of gender
    if 'Gender' in df:
        male_count = df.query('Gender == "Male"').Gender.count()
        female_count = df.query('Gender == "Female"').Gender.count()
        print('There are {:,} male people.\nThere are {:,} female '
              'people.'.format(male_count, female_count))
    else:
        print('Gender is not included in the data.')

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = int(df['Birth Year'].min())
        latest = int(df['Birth Year'].max())
        mode = int(df['Birth Year'].mode())
        print('The oldest people are born in {}.\nThe youngest people are '
              'born in {}.\nThe most popular birth year is '
              '{}.'.format(earliest, latest, mode))
    else:
        print('Birth Year is not included in the data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df, how_many_lines_to_show=5):
    '''Shows x lines of data if the person chooses to show data.
    After showing x lines, ask the person if they would like to see X more
    lines of data and will continue to ask until the person says to stop.

    Args:
        (dataframe)df - Pandas DataFrame to show detail data
        (int)how_many_lines_to_show - How many lines to display per request
    Returns:
        none
    '''

    head = 0
    tail = int(how_many_lines_to_show)
    choices = ('yes', 'no', 'y', 'n')
    choice = ''

    df['Trip Duration'].fillna(0, inplace=True)
    df['User Type'].fillna('', inplace=True)

    if 'Gender' in df:
        df['Gender'].fillna('', inplace=True)

    if 'Birth Year' in df:
        df['Birth Year'].fillna('', inplace=True)

    while choice not in choices:
        choice = input('\nWould you like to see individual trip data ({})?'
                       ' '.format(', '.join(choices).title())).lower()

    while (choice in choices) and (choice not in ('no', 'n')):
        # prints every column except the 'journey' column created
        # in statistics()
        print(df[df.columns[0:-1]].iloc[head:tail])

        choice = ''
        while choice not in choices:
            choice = input('\nWould you like to see more individual trip data '
                           '({})? '.format(', '.join(choices).title())).lower()

            if choice in ('yes', 'y'):
                head += int(how_many_lines_to_show)
                tail += int(how_many_lines_to_show)


def main():
    exit_loop = False
    while exit_loop is False:
        city = get_city()
        if city.lower() != "quit":
            df = load_city(city)
            filter = get_filter()
            if filter.lower() != "quit":
                # if filter.lower() == 'month':
                if filter.lower() in ('month', 'both'):
                    month = get_month()
                    if month.lower() != "quit":
                        df = filter_by_month(df, month)
                    else:
                        exit_loop = True
                # if filter.lower() == 'day':
                if filter.lower() in ('day', 'both'):
                    day = get_day()
                    if day.lower() != "quit":
                        df = filter_by_day(df, day)
                    else:
                        exit_loop = True
            else:
                exit_loop = True
        else:
            exit_loop = True

        if exit_loop is False:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            display_data(df, 5)

            choices = ('yes', 'no', 'y', 'n')
            restart = ''
            while restart not in choices:
                restart = input('\nWould you like to restart ({})?'
                                ' '.format(', '.join(choices).title())).lower()

            if restart in ('no', 'n'):
                exit_loop = True


if __name__ == "__main__":
    main()
