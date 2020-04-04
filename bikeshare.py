import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',  # 1-6
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

FILTER_CHOICES = ('month', 'day', 'both', 'none')

CITY_MONTHS = ('january', 'febuary', 'march', 'april', 'may', 'june', 'all')
#   'july', 'august', 'september', 'october', 'november', 'december'

# CITY_MONTHS = {'january': 1,
#                'febuary': 2,
#                'march': 3,
#                'april': 4,
#                'may': 5,
#                'june': 6}
#   'july': 7,
#   'august': 8,
#   'september': 9,
#   'october': 10,
#   'november': 11,
#   'december': 12}

CITY_DAYS = ('sunday', 'monday', 'tuesday', 'wednesday',
             'thursday', 'friday', 'saturday', 'all')

# CITY_DAYS = {'sunday': 1,
#              'monday': 2,
#              'tuesday': 3,
#              'wednesday': 4,
#              'thursday': 5,
#              'friday': 6,
#              'saturday': 7}


def string_to_Int(value_in, default_value=0):
    try:
        return_value = int(value_in)
    except ValueError:
        return_value = default_value

    return return_value


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_names = list(CITY_DATA.keys())
    city = ''
    FilterChoice = ''
    month = ''
    day = ''

    while ((city.lower() not in city_names) and (city.lower() != 'quit')):
        city = input('Choose a city ({}) or type Quit to exit: '.format(
            ', '.join(city_names).title()))
    # print(city)

    if city != 'quit':
        while ((FilterChoice.lower() not in FILTER_CHOICES) and
               (FilterChoice.lower() != 'quit')):
            FilterChoice = input('Choose a filter type ({}) or type Quit to exit: '.format(
                ', '.join(FILTER_CHOICES).title()))
        # print(FilterChoice)

    if ((FilterChoice.lower() != 'quit') and (FilterChoice.lower() == 'none')):
        month = 'all'
        day = 'all'

    # TO DO: get user input for month (all, january, february, ... , june)
    if ((FilterChoice.lower() != 'quit') and
            (FilterChoice.lower() in ('month', 'both'))):
        while ((month.lower() not in CITY_MONTHS) and
               (month.lower() != 'quit')):
            month_choice = input('Choose a month by name or all for every month ({}) or number (1 = January) or type Quit to exit: '.format(
                ', '.join(CITY_MONTHS).title()))

            if month_choice.isdigit() == True:
                month = CITY_MONTHS[int(month_choice) - 1]
            else:
                month = month_choice
        # print(month)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    if ((month.lower() != 'quit') and
            (FilterChoice.lower() in ('day', 'both'))):
        while ((day.lower() not in CITY_DAYS) and
               (day.lower() != 'quit')):
            day_choice = input('Choose a day of the week by name or all for every day ({}) or number (1 = Sunday) or type Quit to exit: '.format(
                ', '.join(CITY_DAYS).title()))

            if day_choice.isdigit() == True:
                if int(day_choice) in range(1, 8):
                    day = CITY_DAYS[int(day_choice) - 1]
            else:
                day = day_choice
        # print(day)

    print('-'*40)
    return city.lower(), month.lower(), day.lower(), FilterChoice.lower()


def load_data(city, month, day, filter):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

#     print('City: {} -- Month: {} -- day: {}'.format(city, month, day))
#     print(CITY_DATA[city])
#     print('-'*40)

    df = pd.read_csv(CITY_DATA[city], parse_dates=['Start Time', 'End Time'])

    df['journey'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name  # day_name  # weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable

    df_filtered = df.copy()
    if ((filter.lower() in ('month', 'both')) and (month.lower() != 'all')):
        # use the index of the months list to get the corresponding int
        month_index = CITY_MONTHS.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df_filtered = df_filtered[df_filtered['month'] == month_index]
        lower_limit = '2017-{}'.format(month_index)
        uppper_limit = '2017-{}'.format(month_index)
        df_filtered = df_filtered[(df_filtered['Start Time'] >= lower_limit) &
                                  (df_filtered['Start Time'] < uppper_limit)]

    # filter by day of week if applicable
    if ((filter.lower() in ('day', 'both')) and (day.lower() != 'all')):
        print(day.title())
        # filter by day of week to create the new dataframe
        df_filtered = df_filtered[df_filtered['day_of_week'] == day.title()]

    return df_filtered


def time_stats(df, filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    # print("\n{}".format(df.groupby(['month']).agg(
    #     lambda x: x.value_counts().index[0])))
    # common_month = int(df['month'].mean())
    if filter.lower() == 'all':
        common_month = df['month'].mode()[0]
        print("\ncommon month: {}".format(common_month))

    # TO DO: display the most common day of week
#     common_day_of_week = df.groupby(['day_of_week']).agg(
#         lambda x: x.value_counts().index[0])
#     common_day_of_week = df['month'].mode().max()
#     common_day_of_week = df['day_of_week'].mode()[0]
    if filter.lower() in ('day', 'all'):
        common_day_of_week = df['day_of_week'].value_counts().idxmax()
        print("\ncommon day of Week: {}".format(common_day_of_week))

    # TO DO: display the most common start hour
    # df['hour'] = df['Start Time'].dt.hour
    # print("\n{}".format(df.groupby(['hour']).agg(
    #     lambda x: x.value_counts().index[0])))
    common_hour = int(df['hour'].mean())
    # common_hour = df['hour'].mode()[0]
    # common_hour = int(df['Start Time'].dt.hour.mode())
    print("\ncommon hour: {}".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# def station_stats(df):
#     """Displays statistics on the most popular stations and trip."""

#     print('\nCalculating The Most Popular Stations and Trip...\n')
#     start_time = time.time()

#     # TO DO: display most commonly used start station

#     # TO DO: display most commonly used end station

#     # TO DO: display most frequent combination of start station and end station trip

#     print("\nThis took %s seconds." % (time.time() - start_time))
#     print('-'*40)


# def trip_duration_stats(df):
#     """Displays statistics on the total and average trip duration."""

#     print('\nCalculating Trip Duration...\n')
#     start_time = time.time()

#     # TO DO: display total travel time

#     # TO DO: display mean travel time

#     print("\nThis took %s seconds." % (time.time() - start_time))
#     print('-'*40)


# def user_stats(df):
#     """Displays statistics on bikeshare users."""

#     print('\nCalculating User Stats...\n')
#     start_time = time.time()

#     # TO DO: Display counts of user types

#     # TO DO: Display counts of gender

#     # TO DO: Display earliest, most recent, and most common year of birth

#     print("\nThis took %s seconds." % (time.time() - start_time))
#     print('-'*40)


def main():
    while True:
        city, month, day, chosen_filter = get_filters()
#         print('City: {} -- Month: {} -- day: {}'.format(city, month, day))
        if ((city.lower() != "quit") and (month.lower() != "quit") and (day.lower() != "quit")):
            df = load_data(city, month, day, chosen_filter)
            print(df)
#             user_types = df['User Type'].value_counts()
#             print(user_types)
            # time_stats(df, chosen_filter)
        #     station_stats(df)
        #     trip_duration_stats(df)
        #     user_stats(df)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                break
        else:
            break
#         break


if __name__ == "__main__":
    main()
