import React from 'react';
import useLocalStorage from 'use-local-storage';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ProtectedRoute } from './utils/ProtectedRoute';

import './App.css'

import Home from './pages/Home';
import Login from './pages/Login';
import Navbar from './components/navbar/Navbar';
import Booking from './features/booking/pages/Booking';
import StoreList from './features/storeList/pages/StoreList';
import NoPermission from './pages/NoPermission';

const App = () => {

    const defaultDark = window.matchMedia('(prefers-color-sceme: dark)').matches
    const [theme, setTheme] = useLocalStorage('theme', defaultDark ? 'dark' : 'light')

    const switchTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    }

    // const userRoles = fetchUserRoles(); TODO: implement all the necessary fetching
    const userRoles = ['manager']

    return (
        <div className='App' data-theme={theme}>
            <BrowserRouter>
                <Navbar />
                <Routes>
                    <Route exact path='/' element={<Home />} />
                    <Route exact path='/login' element={<Login />} />
                    <Route exact path='/rent' element={<Booking />} />
                    <Route exact path='/store-management' element={<ProtectedRoute roles={['manager', 'admin']} userRoles={userRoles} />}>
                        <Route exact path='/store-management' element={<StoreList />} />
                    </Route>
                    <Route exact path='/no-permission/' element={<NoPermission />} />
                </Routes>
                <button className='dark-theme-button' onClick={switchTheme}>{theme === 'light' ? 'Dark' : 'Light'} mode</button>
            </BrowserRouter>
        </div>
    );
}

export default App;