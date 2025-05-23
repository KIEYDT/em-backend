import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import Signin from './Signin'
import reportWebVitals from './reportWebVitals';
import { ViewEvent, CreateEvent, Event } from './Event';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path='/' element={<Signin />} />
        <Route path='/home' element={<ViewEvent />} />
        <Route path='/create' element={<CreateEvent />} />
        <Route path='/event' element={<Event />} />
      </Routes>
    </Router>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
