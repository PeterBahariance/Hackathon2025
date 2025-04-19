import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Chip } from '@mui/material';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import NightsStayIcon from '@mui/icons-material/NightsStay';
import mockData from '../data/mockData.json';
import ButtonBase from '@mui/material/ButtonBase';

const MedicationSchedule = ({handleMedClick}) => {
    const { medications } = mockData;
    const [currentTime, setCurrentTime] = useState(new Date());

    // Update current time every second
    useEffect(() => {
        const timer = setInterval(() => {
            setCurrentTime(new Date());
        }, 1000);
        return () => clearInterval(timer);
    }, []);

    const formatTime = (time) => {
        if (time instanceof Date) {
            return time.toLocaleTimeString('en-US', {
                hour: 'numeric',
                minute: '2-digit',
                hour12: true
            });
        } else {
            // Handle time string (e.g., "08:00")
            const [hours, minutes] = time.split(':');
            const hour = parseInt(hours);
            const ampm = hour >= 12 ? 'PM' : 'AM';
            const formattedHour = hour % 12 || 12;
            return `${formattedHour}:${minutes} ${ampm}`;
        }
    };

    const getTimeOfDayIcon = (time) => {
        const hour = time.getHours();
        if (hour >= 6 && hour < 12) {
            return <WbSunnyIcon sx={{ color: '#FFA500' }} />; // Morning (6am-12pm)
        } else if (hour >= 12 && hour < 17) {
            return <Brightness4Icon sx={{ color: '#FFD700' }} />; // Afternoon (12pm-5pm)
        } else {
            return <NightsStayIcon sx={{ color: '#4169E1' }} />; // Night (5pm-6am)
        }
    };

    const getTimeStatus = (scheduledTime) => {
        const now = currentTime;
        const diffMinutes = Math.floor((scheduledTime - now) / (1000 * 60));

        if (diffMinutes < 0) return { label: 'Overdue', color: 'error' };
        if (diffMinutes <= 30) return { label: 'Due Soon', color: 'warning' };
        if (diffMinutes <= 60) return { label: 'Upcoming', color: 'info' };
        return { label: 'Scheduled', color: 'success' };
    };

    const formatCountdown = (ms) => {
        if (ms <= 0) return 'Now';

        const hours = Math.floor(ms / (1000 * 60 * 60));
        const minutes = Math.floor((ms % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((ms % (1000 * 60)) / 1000);

        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else if (minutes > 0) {
            return `${minutes}m ${seconds}s`;
        } else {
            return `${seconds}s`;
        }
    };

    // Create an array of all medication instances with their specific times
    const medicationInstances = medications.flatMap(medication => {
        return Array.from({ length: medication.frequency }, (_, i) => {
            const timeKey = `time${i + 1}`;
            const [hours, minutes] = medication[timeKey].split(':');
            const scheduledTime = new Date(currentTime);
            scheduledTime.setHours(parseInt(hours), parseInt(minutes), 0);

            // If the time has passed for today, set it for tomorrow
            if (scheduledTime < currentTime) {
                scheduledTime.setDate(scheduledTime.getDate() + 1);
            }

            return {
                ...medication,
                scheduledTime,
                instanceTime: medication[timeKey]
            };
        });
    });

    // Sort all instances by scheduled time
    const sortedInstances = [...medicationInstances].sort((a, b) =>
        a.scheduledTime - b.scheduledTime
    );

    return (
        <Paper elevation={2} sx={{ p: 2 }}>
            <Box sx={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                mb: 2,
                pb: 2,
                borderBottom: '1px solid rgba(0, 0, 0, 0.12)'
            }}>
                <Typography variant="h6">
                    Current Time: {formatTime(currentTime)}
                </Typography>
            </Box>
            <Box sx={{
                display: 'grid',
                gridTemplateColumns: {
                    xs: '1fr',
                    sm: 'repeat(2, 1fr)',
                    md: 'repeat(3, 1fr)'
                },
                gap: 2
            }}>
                {sortedInstances.map((instance) => {
                    const status = getTimeStatus(instance.scheduledTime);
                    const timeUntilNext = instance.scheduledTime - currentTime;

                    return (
                        <Paper
                            key={`${instance.pillName}-${instance.instanceTime}`}
                            onClick={() => handleMedClick(instance)} // Move onClick here
                            elevation={1}
                            sx={{
                                p: 2,
                                height: '160px',
                                display: 'grid',
                                gridTemplateRows: 'auto 1fr',
                                borderLeft: `4px solid ${status.color === 'error' ? 'red' :
                                    status.color === 'warning' ? 'orange' :
                                        status.color === 'info' ? 'blue' : 'green'}`,
                                cursor: 'pointer',
                                '&:hover': {
                                boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)', // Optional hover effect
                                },
                                transition: 'box-shadow 0.2s ease-in-out'
                            }}
                        >
                            <Box sx={{
                                display: 'flex',
                                alignItems: 'center',
                                gap: 1,
                                height: '32px'
                            }}>
                                <Box sx={{ flex: 1 }}>
                                    <Typography
                                        variant="subtitle1"
                                        sx={{
                                            fontWeight: 600,
                                            overflow: 'hidden',
                                            textOverflow: 'ellipsis',
                                            whiteSpace: 'nowrap'
                                        }}
                                    >
                                        {instance.pillName}
                                    </Typography>
                                    <Typography
                                        variant="caption"
                                        color="text.secondary"
                                        sx={{
                                            display: 'block',
                                            overflow: 'hidden',
                                            textOverflow: 'ellipsis',
                                            whiteSpace: 'nowrap'
                                        }}
                                    >
                                        Dosage: {instance.dosage}
                                    </Typography>
                                </Box>
                                <Chip
                                    label={status.label}
                                    color={status.color}
                                    size="small"
                                />
                            </Box>
                            <Box sx={{
                                display: 'grid',
                                gridTemplateRows: '1fr 1fr',
                                alignItems: 'center'
                            }}>
                                <Box sx={{
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: 1
                                }}>
                                    <Typography
                                        variant="body2"
                                        color="text.primary"
                                        sx={{
                                            overflow: 'hidden',
                                            textOverflow: 'ellipsis',
                                            whiteSpace: 'nowrap'
                                        }}
                                    >
                                        Scheduled at {formatTime(instance.scheduledTime)}
                                    </Typography>
                                    {getTimeOfDayIcon(instance.scheduledTime)}
                                </Box>
                                <Typography
                                    variant="body2"
                                    sx={{
                                        color: timeUntilNext <= 30 * 60 * 1000 ? 'warning.main' : 'text.secondary',
                                        fontWeight: timeUntilNext <= 30 * 60 * 1000 ? 500 : 400,
                                        overflow: 'hidden',
                                        textOverflow: 'ellipsis',
                                        whiteSpace: 'nowrap'
                                    }}
                                >
                                    Time until next dose: {formatCountdown(timeUntilNext)}
                                </Typography>
                            </Box>
                        </Paper>
                    );
                })}
            </Box>
        </Paper>
    );
};

export default MedicationSchedule; 