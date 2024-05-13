import React from 'react';
import useLocalStorage from 'use-local-storage';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProtectedElement } from './utils/ProtectedElement';

import './i18n';

import { MdLightMode } from "react-icons/md";
import { MdDarkMode } from "react-icons/md";

import './App.css'

import Home from './pages/Home';
import Login from './pages/Login';
import Navbar from './components/navbar/Navbar';
import Booking from './features/booking/pages/Booking';
import StoreList from './features/storeList/pages/StoreList';
import NoPermission from './pages/NoPermission';

import LanguageToggle from './components/LanguageToggle';
import UserList from './features/userList/pages/UserList';

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

    return (
        <div className='App' data-theme={theme}>
            <BrowserRouter>
                <Navbar />
                <Routes>
                    <Route exact path='/' element={<Home />} />
                    <Route exact path='/login' element={<Login />} />
                    <Route exact path='/rent' element={<Booking />} />
                    <Route exact path='/store-management' element={<ProtectedElement element={<StoreList />} elementRoles={['manager', 'admin']} userRoles={userRoles} />} />
                    <Route exact path='/users' element={<ProtectedElement element={<UserList />} elementRoles={['admin']} userRoles={userRoles} />} />
                    <Route exact path='/no-permission/' element={<NoPermission />} />
                </Routes>
            </BrowserRouter>
            <div className='side-panel'>
                <LanguageToggle />
                <button className='theme-toggle' onClick={switchTheme}>{theme === 'light' ? <MdLightMode /> : <MdDarkMode />}</button>
            </div>
        </div>
    );
}

export default App;