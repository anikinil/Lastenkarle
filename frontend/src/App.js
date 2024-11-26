import React, { useEffect, useState } from 'react';
import useLocalStorage from 'use-local-storage';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProtectedElement } from './utils/ProtectedElement';

import './i18n';

// TEST

import { MdLightMode } from 'react-icons/md';
import { MdDarkMode } from 'react-icons/md';

import './App.css'
import './components/sidePanel/SidePanel.css'

import Home from './pages/Home';
import Login from './pages/Login';
import Logout from './pages/Logout';
import AccountDeletion from './pages/AccountDeletion';
import UserBan from './features/userBan/pages/UserBan';
import Navbar from './components/navbar/Navbar';
import Booking from './features/booking/pages/Booking';
import BookingPage from './features/bookingDisplay/pages/BookingPage';
import StoreListPage from './features/storeList/pages/StoreListPage';

import LanguageToggle from './components/sidePanel/LanguageToggle';
import UserList from './features/userList/pages/UserList';
import RegionalBooking from './features/booking/pages/RegionalBooking';
import BikeListPage from './features/allBikesList/pages/AllBikesPage';
import BikeRegistration from './features/bikeRegistration/pages/BikeRegistration';
import StoreRegistration from './features/storeRegistration/pages/StoreRegistration';
import BookingList from './features/bookingListAdmin/pages/BookingList';
import BikeConfigPage from './features/bikeConfig/pages/BikeConfigPage';
import Register from './pages/Register';
import Enrollment from './features/enrollment/pages/Enrollment';
import StoreBookings from './features/storeBookings/pages/StoreBookings';

import NavigationError from './pages/NavigationError';
import { BIKE, BIKE_BOOKING, BIKE_REGISTRATION, ALL_BIKES, BOOKING, BOOKINGS, ACCOUNT_DELETION, EMAIL_VERIFICATION, ENROLLMENT, HOME, LOGIN, LOGOUT, REGIONAL_BOOKING, REGISTER, STORE, STORE_BOOKINGS, STORE_REGISTRATION, USER_BAN, USERS, STORE_CONFIG, MY_STORES, ALL_STORES, STORE_DISPLAY, BIKE_CONFIG } from './constants/URLs/Navigation';
import { getCookie } from './services/Cookies';
import { ID, KEY, REGION_NAME, STORE_NAME } from './constants/URLs/General';
import EmailVerification from './pages/EmailVerification';
import { Roles } from './constants/Roles';
import { ERR_FETCHING_USER_DATA, ERR_FETCHING_USER_FLAGS } from './constants/ErrorMessages';
import { USER_DATA } from './constants/URIs/UserURIs';
import AllBikesPage from './features/allBikesList/pages/AllBikesPage';
import AllStoresPage from './features/allStoresPage/pages/AllStoresPage';
import MyStoresPage from './features/myStoresPage/pages/MyStoresPage';
import StoreConfigPage from './features/storeConfig/pages/StoreConfigPage';
import BikeBookingPage from './features/bikeBooking/pages/BikeBookingPage';
import StorePageCustomer from './features/storePageCustomer/pages/StorePageCustomer';
import StoreDisplay from './features/storePageCustomer/pages/StorePageCustomer';

const App = () => {

    // Determine if the user prefers a dark theme
    const defaultDark = window.matchMedia('(prefers-color-sceme: dark)').matches
    const [theme, setTheme] = useLocalStorage('theme', defaultDark ? 'dark' : 'light')

    // Function to switch between light and dark themes
    const switchTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    }

    return (
        <div className='App' data-theme={theme}>
            <div className='content-container'>
                <BrowserRouter>
                    <Navbar />
                    <Routes>

                        <Route exact path={HOME} element={<Home />} />

                        {/* ACCOUNTS */}

                        <Route exact path={LOGIN} element={<Login />} />
                        <Route exact path={LOGOUT} element={<Logout />} />
                        <Route exact path={ACCOUNT_DELETION} element={<AccountDeletion />} />
                        <Route exact path={REGISTER} element={<Register />} />
                        <Route exact path={EMAIL_VERIFICATION.replace(ID, ':id').replace(KEY, ':key')} element={<EmailVerification />} />
                        <Route exact path={ENROLLMENT} element={
                            <ProtectedElement element={<Enrollment />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                        } />
                        <Route exact path={USER_BAN} element={
                            <ProtectedElement element={<UserBan />} elementRoles={[Roles.MANAGER]} />
                        } />
                        <Route exact path={USERS} element={
                            <ProtectedElement element={<UserList />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                        } />

                        {/* BOOKING */}

                        <Route exact path={BOOKING} element={<Booking />} />
                        <Route path={REGIONAL_BOOKING.replace(REGION_NAME, ':region')} element={<RegionalBooking />} />
                        <Route exact path={BIKE_BOOKING.replace(ID, ':bike')} element={<BikeBookingPage />} />

                        {/* STORES */}

                        <Route exact path={MY_STORES} element={
                            <ProtectedElement element={<MyStoresPage />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                        } />
                        <Route exact path={STORE_DISPLAY.replace(ID, ':id')} element={<StoreDisplay />} />
                        <Route exact path={ALL_STORES} element={
                            <ProtectedElement element={<AllStoresPage />} elementRoles={[Roles.ADMINISTRATOR]} />
                        } />
                        <Route exact path={STORE_CONFIG.replace(STORE_NAME, ':store')} element={
                            <ProtectedElement element={<StoreConfigPage />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                        } />
                        <Route exact path={STORE_REGISTRATION} element={
                            <ProtectedElement element={<StoreRegistration />} elementRoles={[Roles.ADMINISTRATOR]} />
                        } />

                        {/* BIKES */}

                        <Route exact path={ALL_BIKES} element={
                            <ProtectedElement element={<AllBikesPage />} elementRoles={[Roles.ADMINISTRATOR]} />
                        } />
                        {/* TODO make inaccessible by just entering the store name in search bar by manager of different store */}
                        <Route exact path={BIKE_REGISTRATION.replace(STORE_NAME, ':store')} element={
                            <ProtectedElement element={<BikeRegistration />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                        } />
                        <Route exact path={BIKE_CONFIG.replace(ID, ':id')} element={
                            <ProtectedElement element={<BikeConfigPage />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                        } />

                        {/* BOOKINGS */}

                        {/* <Route exact path={BOOKING_PAGE} element={<BookingPage />} /> */}
                        <Route exact path={BOOKINGS} element={<BookingList />} />
                        <Route exact path={STORE_BOOKINGS} element={
                            <ProtectedElement element={<StoreBookings />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                        } />

                    </Routes>
                </BrowserRouter>
            </div>
            <div className='side-panel'>
                <LanguageToggle />
                <button className='toggle theme' onClick={switchTheme}>{theme === 'light' ? <MdLightMode /> : <MdDarkMode />}</button>
            </div>
        </div >
    );
}

export default App;