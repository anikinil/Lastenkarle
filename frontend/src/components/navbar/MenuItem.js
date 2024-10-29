import React, { useState } from 'react';
import Dropdown from './Dropdown';

// a single menu item
const MenuItem = ({ className, item, userRoles }) => {

    const hasPermission = (item) => {
        console.log('item', item)
        console.log('userRoles', userRoles)
        // console.log(userRoles.some(role => item.roles.includes(role)))
        return userRoles.some(role => item.roles.includes(role));
    }

    const [dropdown, setDropdown] = useState(false);

    return (
        <>
            {hasPermission(item) ? (

                item.submenu ? (
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
                    <a className={className} href={item.url}>{item.title}</a>
                )) :
                null
            }
        </>
    )
}

export default MenuItem;