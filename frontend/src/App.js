import React, { Suspense, useEffect } from 'react';
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
import Navbar from './components/navbar/Navbar';
import Renting from './features/renting/pages/Renting';

import LanguageToggle from './components/sidePanel/LanguageToggle';
import RegionalRenting from './features/renting/pages/RegionalRenting';
import BikeRegistration from './features/bikeRegistration/pages/BikeRegistration';
import StoreRegistration from './features/storeRegistration/pages/StoreRegistration';
import BookingList from './features/bookingListAdmin/pages/BookingList';
import BikeConfigPage from './features/bikeConfig/pages/BikeConfigPage';
import Register from './pages/Register';
import Enrollment from './features/enrollment/pages/Enrollment';
import StoreBookings from './features/storeBookings/pages/StoreBookings';

import { BIKE_RENTING, BIKE_REGISTRATION, ALL_BIKES, RENTING, ACCOUNT_DELETION, EMAIL_VERIFICATION, 
    ENROLLMENT, HOME, LOGIN, LOGOUT, REGIONAL_RENTING, REGISTER, STORE_BOOKINGS, STORE_REGISTRATION, 
    STORE_CONFIG, MY_STORES, ALL_STORES, BIKE_CONFIG, ALL_BOOKINGS, ALL_USERS, USER_PAGE, STORE_PAGE_OF_BIKE} 
    from './constants/URLs/Navigation';
    
import { ID, KEY, REGION_NAME, STORE_NAME } from './constants/URLs/General';
import EmailVerification from './pages/EmailVerification';
import { Roles } from './constants/Roles';
import AllBikesPage from './features/allBikesList/pages/AllBikesPage';
import AllStoresPage from './features/allStoresPage/pages/AllStoresPage';
import MyStoresPage from './features/myStoresPage/pages/MyStoresPage';
import StoreConfigPage from './features/storeConfig/pages/StoreConfigPage';
import BikeRentingPage from './features/renting/pages/BikeRentingPage';
import { AuthProvider } from './AuthProvider';
import UserListPage from './features/userList/pages/UserListPage';
import PageNotFound from './pages/PageNotFound';
import Loading from './pages/loading/Loading';
import { tokenExpired } from './services/Token';
import { setCookie } from './services/Cookies';
import UserPage from './features/userPage/UserPage';
import StorePageCustomer from './features/storePage/pages/StorePageCustomer';

// TODO fix region selection everywhere

// TODO fix region selection everywhere

// THINK look into AuthService for login and logout
const App = () => {

    // Determine if the user prefers a dark theme
    const defaultDark = window.matchMedia('(prefers-color-sceme: dark)').matches
    const [theme, setTheme] = useLocalStorage('theme', defaultDark ? 'dark' : 'light')

    let location = window.location.pathname;
    
    // Function to switch between light and dark themes
    const switchTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    }

    // THINK if some sort of encapsulation needed
    // TODO maybe add a notification when session expired (may be with a button leading to the login page)
    // on page load, check if the token is expired and reset the user roles and stores, to update the navbar
    useEffect(() => {
        if (tokenExpired()) {
            setCookie('userRoles', [Roles.VISITOR]);
            setCookie('userStores', []);
        }
    }, [location])

    return (
        <div className='App' data-theme={theme}>
            <div className='content-container'>
                <AuthProvider>
                    <Suspense fallback={<Loading />}>
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
                                {/* <Route exact path={USER_BAN} element={
                                {/* <Route exact path={USER_BAN} element={
                                    <ProtectedElement element={<UserBan />} elementRoles={[Roles.MANAGER]} />
                                } /> */}
                                <Route exact path={ALL_USERS} element={
                                    <ProtectedElement element={<UserListPage />} elementRoles={[Roles.ADMINISTRATOR]} />
                                } />
                                <Route exact path={USER_PAGE.replace(ID, ':user')} element={
                                    <ProtectedElement element={<UserPage />} elementRoles={[Roles.ADMINISTRATOR]} />
                                } />

                                {/* RENTING */}

                                <Route exact path={RENTING} element={<Renting />} />
                                <Route path={REGIONAL_RENTING.replace(REGION_NAME, ':region')} element={<RegionalRenting />} />
                                <Route exact path={BIKE_RENTING.replace(ID, ':bike')} element={<BikeRentingPage />} />

                                {/* STORES */}

                                <Route exact path={MY_STORES} element={
                                    <ProtectedElement element={<MyStoresPage />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                                } />
                                <Route exact path={STORE_PAGE_OF_BIKE.replace(ID, ':bike')} element={<StorePageCustomer />} />
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
                                <Route exact path={ALL_BOOKINGS} element={
                                    <ProtectedElement element={<BookingList />} elementRoles={[Roles.ADMINISTRATOR]} />
                                } />
                                <Route exact path={STORE_BOOKINGS} element={
                                    <ProtectedElement element={<StoreBookings />} elementRoles={[Roles.ADMINISTRATOR, Roles.MANAGER]} />
                                } />

                                {/* OTHER */}

                                <Route path='*' element={<PageNotFound />} />
                            
                            </Routes>
                        </BrowserRouter>
                    </Suspense>
                </AuthProvider>
            </div>
            <div className='side-panel'>
                <LanguageToggle />
                <button className='toggle theme' onClick={switchTheme}>{theme === 'light' ? <MdDarkMode /> : <MdLightMode />}</button>
            </div>
        </div >
    );
}

export default App;