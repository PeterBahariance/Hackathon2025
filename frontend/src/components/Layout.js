import React from 'react';
import { AppBar, Toolbar, Typography, Box, Container } from '@mui/material';

const Layout = ({ children }) => {
    return (
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                        Medication Tracker
                    </Typography>
                </Toolbar>
            </AppBar>

            <Container component="main" sx={{ mt: 4, mb: 4, flex: 1 }}>
                {children}
            </Container>

            <Box
                component="footer"
                sx={{
                    py: 3,
                    px: 2,
                    mt: 'auto',
                    backgroundColor: (theme) => theme.palette.grey[200],
                }}
            >
                <Container maxWidth="sm">
                    <Typography variant="body2" color="text.secondary" align="center">
                        © {new Date().getFullYear()} Medication Tracker. All rights reserved.
                    </Typography>
                </Container>
            </Box>
        </Box>
    );
};

export default Layout; 