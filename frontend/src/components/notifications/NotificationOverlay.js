import React from 'react';

import './NotificationOverlay.css';

const NotificationOverlay = ({ message, type }) => {

  return (
    <div className={`notification-overlay ${type}`}>
        {message}
    </div>
  );
};

export default NotificationOverlay;
