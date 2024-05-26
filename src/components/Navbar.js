import React, { useState, useEffect, useContext } from 'react';
import { Button } from './Button';
import { Link, useNavigate } from 'react-router-dom';
import './Navbar.css';
import AuthContext from './pages/Sign In/AuthContext';
function Navbar() {
    const [click, setClick] = useState(false);
    const [button, setButton] = useState(true);
    const navigate = useNavigate();

    // Use AuthContext
    const { logout } = useContext(AuthContext);

    const handleClick = () => setClick(!click);
    const closeMobileMenu = () => setClick(false);

    const showButton = () => {
        if (window.innerWidth <= 960) {
            setButton(false);
        } else {
            setButton(true);
        }
    };

    useEffect(() => {
        showButton();
        const handleResize = () => showButton();
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    const handleLogout = async () => {
        try {
          const response = await fetch('http://localhost:5000/auth/logout', {
            method: 'GET',
            credentials: 'include'
        });
        
            const data = await response.json();
            if (response.ok) {
                console.log('Logout successful:', data.message);
                logout();  // Update the context to reflect logout
                navigate('/login');
            } else {
                console.error('Logout failed:', data.message);
            }
        } catch (error) {
            console.error('Network error on logout:', error);
        }
    };

    return (
        <>
            <nav className='navbar'>
                <div className='navbar-container'>
                    <Link to='/' className='navbar-logo' onClick={closeMobileMenu}>
                        Uniguide<i className='fab fa-typo3' />
                    </Link>
                    <div className='menu-icon' onClick={handleClick}>
                        <i className={click ? 'fas fa-times' : 'fas fa-bars'} />
                    </div>
                    <ul className={click ? 'nav-menu active' : 'nav-menu'}>
                        <li className='nav-item'>
                            <Link to='/' className='nav-links' onClick={closeMobileMenu}>Home</Link>
                        </li>
                        <li className='nav-item'>
                            <Link to='/notes' className='nav-links' onClick={closeMobileMenu}>Notes</Link>
                        </li>
                        <li className='nav-item'>
                            <Link to='/about-us' className='nav-links' onClick={closeMobileMenu}>About Us</Link>
                        </li>
                        <li className='nav-item'>
                            <Link to='/contact-us' className='nav-links' onClick={closeMobileMenu}>Contact Us</Link>
                        </li>
                        <li className='nav-item'>
                            <Link to='/saved-conversations' className='nav-links' onClick={closeMobileMenu}>Archived Chats</Link>
                        </li>
                        {button && <li><Button buttonStyle='btn--outline' onClick={handleLogout}>LOG OUT</Button></li>}
                    </ul>
                </div>
            </nav>
        </>
    );
}

export default Navbar;
