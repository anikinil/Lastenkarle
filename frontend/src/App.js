import React, { useEffect, useState } from 'react';
import useLocalStorage from 'use-local-storage';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProtectedElement } from './utils/ProtectedElement';

import './i18n';

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
import BikeBooking from './features/booking/pages/BikeBooking';
import StorePage from './features/storeDisplay/pages/StorePage';
import StoreConfigPage from './features/storeConfig/pages/StoreConfigPage';
import BikeListPage from './features/bikeList/pages/BikeListPage';
import BikeRegistration from './features/bikeRegistration/pages/BikeRegistration';
import StoreRegistration from './features/storeRegistration/pages/StoreRegistration';
import BookingList from './features/bookingListAdmin/pages/BookingList';
import BikePage from './features/bikeDisplay/pages/BikePage';
import BikeConfigPage from './features/bikeConfig/pages/BikeConfigPage';
import Register from './pages/Register';
import Enrollment from './features/enrollment/pages/Enrollment';
import StoreBookings from './features/storeBookings/pages/StoreBookings';

import NavigationError from './pages/NavigationError';
import { BIKE, BIKE_BOOKING, BIKE_REGISTRATION, BIKES, BOOKING, BOOKINGS, ACCOUNT_DELETION, EMAIL_VERIFICATION, ENROLLMENT, HOME, LOGIN, LOGOUT, REGIONAL_BOOKING, REGISTER, STORE, STORE_BOOKINGS, STORE_REGISTRATION, STORES, USER_BAN, USERS } from './constants/URLs/Navigation';
import { getCookie } from './services/Cookies';
import { ID, KEY, REGION_NAME, STORE_NAME } from './constants/URLs/General';
import EmailVerification from './pages/EmailVerification';
import { Roles } from './constants/Roles';
import { ERR_FETCHING_USER_DATA, ERR_FETCHING_USER_FLAGS } from './constants/ErrorMessages';
import { USER_DATA } from './constants/URIs/UserURIs';

const App = () => {

    // Determine if the user prefers a dark theme
    const defaultDark = window.matchMedia('(prefers-color-sceme: dark)').matches
    const [theme, setTheme] = useLocalStorage('theme', defaultDark ? 'dark' : 'light')

    // Function to switch between light and dark themes
    const switchTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    }

    // Get the appropriate version of a page by path based on user role
    const getComponentByPath = (path) => {
        // switch (path) {
        //     case '/bike/:id':
        //         if (userRoles.includes('admin') || userRoles.includes('manager')) { return <BikeConfigPage /> }
        //         else { return <BikePage /> }
        //     case '/store/:id':
        //         if (userRoles.includes('admin') || userRoles.includes('manager')) { return <StoreConfigPage /> }
        //         else { return <StorePage /> }
        //     default:
        //         return <NavigationError />
        // }
    }

    return (
        <div className='App' data-theme={theme}>
            <div className='content-container'>
                <BrowserRouter>
                    <Navbar />
                    <Routes>
                        <Route exact path={HOME} element={<Home />} />
                        <Route exact path={LOGIN} element={<Login />} />
                        <Route exact path={LOGOUT} element={<Logout />} />
                        <Route exact path={ACCOUNT_DELETION} element={<AccountDeletion />} />
                        <Route exact path={REGISTER} element={<Register />} />
                        <Route exact path={EMAIL_VERIFICATION.replace(ID, ':id').replace(KEY, ':key')} element={<EmailVerification />} />
                        <Route exact path={USER_BAN} element={
                            <ProtectedElement element={<UserBan />} elementRoles={[Roles.MANAGER]} />
                        } />
                        <Route exact path={BOOKING} element={<Booking />} />
                        {/* <Route exact path={BOOKING} element={<BookingPage />} /> */}
                        <Route exact path={STORES} element={
                            <ProtectedElement element={<StoreListPage />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                        } />
                        <Route exact path={USERS} element={
                            <ProtectedElement element={<UserList />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                        } />
                        <Route path={REGIONAL_BOOKING.replace(REGION_NAME, ':region')} element={<RegionalBooking />} />
                        <Route exact path={BIKE_BOOKING} element={<BikeBooking />} />
                        <Route exact path={BIKES} element={<BikeListPage />} />
                        {/* <Route exact path={BIKE} element={getComponentByPath(BIKE)} /> */}
                        <Route exact path={'/bike/1'} element={<BikePage />} />
                        {/* TODO make inaccessible by just entering the store name in search bar by manager of different store */}
                        <Route exact path={BIKE_REGISTRATION.replace(STORE_NAME, ':store')} element={
                            <ProtectedElement element={<BikeRegistration />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                        } />
                        <Route exact path={STORE_REGISTRATION} element={
                            <ProtectedElement element={<StoreRegistration />} elementRoles={[Roles.ADMINISTRATOR]} />
                        } />

                        <Route exact path={ENROLLMENT} element={
                            <ProtectedElement element={<Enrollment />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                        } />
                        <Route exact path={BOOKINGS} element={<BookingList />} />
                        <Route exact path={STORE.replace(STORE_NAME, ':store')} element={<StoreConfigPage />} />
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