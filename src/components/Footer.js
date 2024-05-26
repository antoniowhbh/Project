import React from 'react';
import './Footer.css';
import { Link } from 'react-router-dom';

function Footer() {
  return (
    <footer className='footer-container'>
      <div className='footer-content'>
        <div className='footer-logo'>
         
        </div>
        <div className='footer-social-media'>
          <Link className='social-icon' to='/' target='_blank' aria-label='Facebook'>
            <i className='fab fa-facebook-f' />
          </Link>
          <Link className='social-icon' to='/' target='_blank' aria-label='Instagram'>
            <i className='fab fa-instagram' />
          </Link>
          <Link className='social-icon' to='/' target='_blank' aria-label='Youtube'>
            <i className='fab fa-youtube' />
          </Link>
          
          <Link className='social-icon' to='/' target='_blank' aria-label='LinkedIn'>
            <i className='fab fa-linkedin' />
          </Link>
        </div>
        <div className='footer-bottom'>
          <small className='website-rights'>Uniguide © 2024</small>
          <div className='footer-terms'>
            <Link to='/terms-of-service'>Terms of Service</Link>
            <Link to='/privacy-policy'>Privacy Policy</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
