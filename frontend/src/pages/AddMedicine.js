import React, { useState, useRef, useEffect } from 'react';
import { Box, Typography, Paper, Button, CircularProgress, Alert } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import CameraAltIcon from '@mui/icons-material/CameraAlt';
import { useNavigate } from 'react-router-dom';

const AddMedicine = () => {
    const navigate = useNavigate();
    const [isDetecting, setIsDetecting] = useState(false);
    const [detectedText, setDetectedText] = useState('');
    const [error, setError] = useState('');
    const videoRef = useRef(null);

    const startDetection = async () => {
        try {
            setIsDetecting(true);
            setError('');

            // Here we would make an API call to the backend to start the label detection
            // For now, we'll simulate the process
            const response = await fetch('http://localhost:5000/api/detect-label', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
            });

            if (!response.ok) {
                throw new Error('Failed to start detection');
            }

            const data = await response.json();
            setDetectedText(data.text || 'No text detected');
        } catch (err) {
            setError(err.message);
        } finally {
            setIsDetecting(false);
        }
    };

    return (
        <Box sx={{ p: 3, maxWidth: '800px', margin: '0 auto' }}>
            <Button
                startIcon={<ArrowBackIcon />}
                onClick={() => navigate('/')}
                sx={{ mb: 3 }}
            >
                Back to Home
            </Button>

            <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
                <Typography variant="h4" gutterBottom>
                    Add New Medicine
                </Typography>
                <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                    Use your camera to scan the medication label. Make sure the label is clearly visible and well-lit.
                </Typography>

                <Box sx={{
                    position: 'relative',
                    width: '100%',
                    height: '400px',
                    backgroundColor: '#f5f5f5',
                    borderRadius: 1,
                    overflow: 'hidden',
                    mb: 3
                }}>
                    <video
                        ref={videoRef}
                        autoPlay
                        playsInline
                        style={{
                            width: '100%',
                            height: '100%',
                            objectFit: 'cover'
                        }}
                    />
                    {isDetecting && (
                        <Box sx={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            backgroundColor: 'rgba(0, 0, 0, 0.5)'
                        }}>
                            <CircularProgress />
                        </Box>
                    )}
                </Box>

                <Button
                    variant="contained"
                    color="primary"
                    startIcon={<CameraAltIcon />}
                    onClick={startDetection}
                    disabled={isDetecting}
                    fullWidth
                    sx={{ mb: 3 }}
                >
                    {isDetecting ? 'Detecting...' : 'Start Detection'}
                </Button>

                {error && (
                    <Alert severity="error" sx={{ mb: 3 }}>
                        {error}
                    </Alert>
                )}

                {detectedText && (
                    <Paper elevation={1} sx={{ p: 2, backgroundColor: '#f8f9fa' }}>
                        <Typography variant="h6" gutterBottom>
                            Detected Text:
                        </Typography>
                        <Typography variant="body1" style={{ whiteSpace: 'pre-wrap' }}>
                            {detectedText}
                        </Typography>
                    </Paper>
                )}
            </Paper>
        </Box>
    );
};

export default AddMedicine; 