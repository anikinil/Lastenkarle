import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import Home from './pages/Home';
import Login from './pages/Login';
import Navbar from './components/Navbar/Navbar';
import Booking from './features/booking/pages/Booking';
import StoreList from './features/storeList/pages/StoreList';

const App = () => {
  return (
    <BrowserRouter>
        <Navbar/>
        <Routes>
            <Route path='/' element={<Home/>}/>
            <Route path='/login' element={<Login/>}/>
            <Route path='/booking' element={<Booking/>}/>
            <Route path='/store-list' element={<StoreList/>}/>
        </Routes>
    </BrowserRouter>
  );
}

export default App;