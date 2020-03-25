#Christopher Hansen
#Programming for Data Science with Python - Udacity

import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ('january', 'february', 'march', 'april', 'may', 'june')

days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        prompt = '\nPlease enter the city you would like to examine (Chicago, New York City, Washington):\n'
        choice = input(prompt).lower().strip()

        if choice in CITY_DATA.keys():
            city = choice
            break
        else:
            print('Incorrect input. Please try again.')

    # get user input for month (all, january, february, ... june)
    while True:
        prompt = '\nPlease enter the month you would like to examine (All, January, February, ... June):\n'
        choice = input(prompt).lower().strip()

        if (choice in months) or (choice == 'all'):
            month = choice
            break
        else:
            print('Incorrect input. Please try again.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        prompt = '\nPlease enter the day you would like to examine (All, Monday, Tuesday, ... Sunday):\n'
        choice = input(prompt).lower().strip()

        if (choice in days) or (choice == 'all'):
            day = choice
            break
        else:
            print('Incorrect input. Please try again.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load the csv file into dataframe and choose the correct columns
    #df = pd.read_csv(CITY_DATA[city], usecols=['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type'])
    df = pd.read_csv(CITY_DATA[city])

    # add columns to make filtering by month and day of week easier
    df['Month'] = pd.DatetimeIndex(df['Start Time']).month
    df['DayOfWeek'] = pd.DatetimeIndex(df['Start Time']).dayofweek
    df['Hour'] = pd.DatetimeIndex(df['Start Time']).hour

    # by month and day of week (month indexes start at 1, day indexes start at 0 (sunday))
    if month != 'all':
        df = df[df['Month'] == (months.index(month) + 1)]

    if day != 'all':
        df = df[df['DayOfWeek'] == days.index(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['Month'].mode()[0]
    print(months[most_common_month - 1] + ' is the month with the most trips taken in the filtered data.')

    # display the most common day of week
    most_common_day = df['DayOfWeek'].mode()[0]
    print(days[most_common_day] + ' is the day of the week with the most trips taken in the filtered data.')

    # display the most common start hour
    start_hour = df['Hour'].mode()[0]
    if start_hour < 12:
        am_time = True
    else:
        am_time = False

    if am_time:
        print(str(start_hour) + ' am is the hour with the most trips taken in the filtered data.')
    else:
        print(str(start_hour - 12) + ' pm is the hour with the most trips taken in the filtered data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = str(df['Start Station'].mode()[0])
    print(most_common_start_station + ' is the most common start station in the filtered data.')

    # display most commonly used end station
    most_common_end_station = str(df['Start Station'].mode()[0])
    print(most_common_end_station + ' is the most common end station in the filtered data.')

    # display most frequent combination of start station and end station trip
    df['Trip'] = (df['Start Station'] + ' to ' + df['End Station'])
    most_common_trip = str(df['Trip'].mode()[0])
    print(most_common_trip + ' is the most common trip made in the filtered data.')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_seconds = df['Trip Duration'].sum()
    years = int(total_travel_seconds // 31536000)
    days = int((total_travel_seconds % 31536000) // 86400)
    hours = int(((total_travel_seconds % 31536000) % 86400) // 3600)
    minutes = int((((total_travel_seconds % 31536000) % 86400) % 3600) // 60)
    seconds = int(((((total_travel_seconds % 31536000) % 86400) % 3600) % 60))

    if (years > 0):
        print('Total travel time: ' + str(years) + ' years, ' + str(days) + ' days, ' + str(hours) + ' hours, ' + str(minutes) + ' minutes, and ' + str(seconds) + ' seconds.')
    else:
        print('Total travel time: ' + str(days) + ' days, ' + str(hours) + ' hours, ' + str(minutes) + ' minutes, and ' + str(seconds) + ' seconds.')

    # display mean travel time
    mean_travel_seconds = df['Trip Duration'].mean()
    days = int(mean_travel_seconds // 86400)
    hours = int((mean_travel_seconds % 86400) // 3600)
    minutes = int(((mean_travel_seconds % 86400) % 3600) // 60)
    seconds = int((((mean_travel_seconds % 86400) % 3600) % 60))

    print('Mean travel time: ' + str(minutes) + ' minutes and ' + str(seconds) + ' seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    if ('Gender' not in df.columns) or ('Birth Year') not in df.columns:
        print('\nUser Stats not available for this data set.\n')
        return

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nDistribution of user types:")
    #print(user_types)
    for name, val in user_types.iteritems():
        print(name + ': ' + str(val))

    # Display counts of gender
    genders = df['Gender'].value_counts()
    print("\nDistribution of genders:")
    #print(genders)
    for name, val in genders.iteritems():
        print(name + ': ' + str(val))

    # Display earliest, most recent, and most common year of birth
    earliest = int(df['Birth Year'].min())
    print('\nEarliest Birth Year: ' + str(earliest))

    most_recent = int(df['Birth Year'].max())
    print('\nMost Recent Birth Year: ' + str(most_recent))

    most_common = int(df['Birth Year'].mode()[0])
    print('\nMost Common Birth Year: ' + str(most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays five rows of raw data for every request by the user"""

    prompt = '\nWould you like to print 5 more lines of raw data? Enter yes or no.\n'
    place = 0

    while True:
        choice = input(prompt).lower().strip()
        if choice not in ('yes', 'ye', 'y'):
            break

        print(df.iloc[place:place + 5].to_string())
        place += 5

    print('-'*40)
	


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
