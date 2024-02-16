// Header.js

import React from 'react';
import { AppBar, Toolbar, Typography, IconButton, Menu, MenuItem } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

function Header() {
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  return (
    <div className="header-container">
      <AppBar position="static">
        <Toolbar>
          <div className="menu-container">
            <div className="title-container">
              <Typography variant="h6" component="div">
                <a href="#" className="home-link">World News</a>
              </Typography>
            </div>
            <nav>
              <ul>
                <li>
                  <IconButton
                    size="large"
                    edge="start"
                    color="inherit"
                    aria-label="menu"
                    onClick={handleMenuOpen}
                    sx={{ mr: 2 }}
                  >
                    <MenuIcon />
                  </IconButton>
                  <Menu
                    id="menu-appbar"
                    anchorEl={anchorEl}
                    open={Boolean(anchorEl)}
                    onClose={handleMenuClose}
                  >
                    <MenuItem onClick={handleMenuClose}><a href="#">USA</a></MenuItem>
                    <MenuItem onClick={handleMenuClose}><a href="#">Russia</a></MenuItem>
                    {/* Остальные страны */}
                    {/* ... */}
                  </Menu>
                </li>
              </ul>
            </nav>
          </div>
        </Toolbar>
      </AppBar>
    </div>
  );
}

export default Header;
