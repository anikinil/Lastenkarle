import React from 'react';
import useLocalStorage from 'use-local-storage';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import './App.css'

import Home from './pages/Home';
import Login from './pages/Login';
import Navbar from './components/Navbar/Navbar';
import Booking from './features/booking/pages/Booking';
import StoreList from './features/storeList/pages/StoreList';

const App = () => {

    const defaultDark = window.matchMedia('(prefers-color-sceme: dark)').matches
    const [theme, setTheme] = useLocalStorage('theme', defaultDark ? 'dark' : 'light')

    const switchTheme = () => {
        const newTheme = theme === 'light' ? 'dark' : 'light';
        setTheme(newTheme);
    } 

    return (
        <div className='App' data-theme={theme}>
            <BrowserRouter>
                <Navbar/>
                <Routes>
                    <Route path='/' element={<Home/>}/>
                    <Route path='/login' element={<Login/>}/>
                    <Route path='/booking' element={<Booking/>}/>
                    <Route path='/store-list' element={<StoreList/>}/>
                </Routes>
                <button className='dark-theme-button' onClick={switchTheme}>{theme === 'light' ? 'Dark' : 'Light'} mode</button>
            </BrowserRouter>
        </div>
    );
}

export default App;