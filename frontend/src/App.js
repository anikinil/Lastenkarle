import React from 'react';
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
import BookingList from './features/bookingList/pages/BookingList';
import BikePage from './features/bikeDisplay/pages/BikePage';
import BikeConfigPage from './features/bikeConfig/pages/BikeConfigPage';
import Logout from './pages/Logout';
import Register from './pages/Register';
import Enrollment from './features/enrollment/pages/Enrollment';

import NavigationError from './pages/NavigationError';

const App = () => {

    console.log()

    const defaultDark = window.matchMedia('(prefers-color-sceme: dark)').matches
    const [theme, setTheme] = useLocalStorage('theme', defaultDark ? 'dark' : 'light')

    const switchTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    }
    // const userRoles = fetchUserRoles(); TODO: implement all the necessary fetching
    const userRoles = ['admin']

    // gets appropriate version of a page by path based on user role
    const getComponentByPath = (path) => {
        switch (path) {
            case '/bike/:id':
                if (userRoles.includes('admin') || userRoles.includes('manager')) { return <BikeConfigPage /> }
                else { return <BikePage /> }
            case '/store/:id':
                if (userRoles.includes('admin') || userRoles.includes('manager')) { return <StoreConfigPage /> }
                else { return <StorePage /> }
            default:
                return <NavigationError />
        }
    }


    return (
        <div className='App' data-theme={theme}>
            <Navbar />
            <div className='content-container'>
                <BrowserRouter>
                    <Routes>
                        <Route exact path='/' element={<Home />} />
                        <Route exact path='/login' element={<Login />} />
                        <Route exact path='/logout' element={<Logout />} />
                        <Route exact path='/register' element={<Register />} />
                        <Route exact path='/user-ban' element={<UserBan />} />
                        <Route exact path='/booking' element={<Booking />} />
                        <Route exact path='/booking/:id' element={<BookingPage />} />
                        <Route exact path='/stores' element={
                            <ProtectedElement element={<StoreListPage />} elementRoles={['admin', 'manager']} userRoles={userRoles} />
                        } />
                        <Route exact path='/users' element={
                            <ProtectedElement element={<UserList />} elementRoles={['admin']} userRoles={userRoles} />
                        } />
                        <Route exact path='/:id' element={<RegionalBooking />} />
                        <Route exact path='/bike-booking' element={<BikeBooking />} />
                        <Route exact path='/bikes' element={<BikeListPage />} />
                        
                        <Route exact path='/bike/:id' element={getComponentByPath('/bike/:id')} />

                        <Route exact path='/bike-registration' element={<BikeRegistration />} />

                        <Route exact path='/store-registration' element={<StoreRegistration />} />
                        <Route exact path='/enrollment' element={<Enrollment />} />
                        <Route exact path='/bookings' element={<BookingList />} />

                        {/* TODO make a seperate file with all paths */}
                        <Route exact path='/store/:id' element={getComponentByPath('/store/:id')} />

                        <Route exact path='/store/:id/bookings' element={
                            <ProtectedElement element={<StoreBookings />} elementRoles={['admin', 'manager']} userRoles={userRoles} />
                        } />
                    </Routes>
                </BrowserRouter>
            </div>
            <div className='side-panel'>
                <LanguageToggle />
                <button className='toggle theme' onClick={switchTheme}>{theme === 'light' ? <MdLightMode /> : <MdDarkMode />}</button>
            </div>
        </div>
    );
}

export default App;