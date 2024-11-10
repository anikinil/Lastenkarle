import React, { useState } from 'react';
import Dropdown from './Dropdown';

// a single menu item
const MenuItem = ({ className, item }) => {

    console.log('item', item);
    console.log('className', className);

    const [dropdown, setDropdown] = useState(false);

    return (
        <>
            {item.submenu ? (
                console.log('submenu', item.submenu),
                <div
                    onMouseLeave={() => setDropdown(false)}
                >
                    <a className={className}
                        aria-haspopup='menu'
                        aria-expanded={dropdown ? 'true' : 'false'}
                        href={item.url}
                        style={item.url ? { cursor: 'pointer' } : { cursor: 'default' }}
                        onMouseEnter={() => setDropdown(true)}
                    >
                        {item.title}
                    </a>
                    <Dropdown
                        submenus={item.submenu}
                        dropdown={dropdown}
                        onClick={() => setDropdown(false)}
                    />
                </div>
            ) : (
                <a
                    className={className}
                    href={item.url}
                >
                    {item.title}
                </a>
            )}
        </>
    )
}

export default MenuItem;