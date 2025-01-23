// A panel to display simple data, like date, booking comment, equipment list etc.
import React from 'react';


// TODO make unhoverable when no handleClick passed (maybe in DisplayPanel.css)

const DisplayPanel = ({ content, handleClick }) => {

    return (
        <li className='list-item' onClick={handleClick}>
            {content}
        </li>
    );
};

export default DisplayPanel;