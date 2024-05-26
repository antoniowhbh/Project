import { useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:5000', {
    transports: ['websocket'], // force WebSocket transport
    upgrade: false // no upgrading to WebSocket from other transports
});

function useSocket() {
    useEffect(() => {
        socket.on('connect', () => {
            console.log('Connected to server via WebSocket');
        });

        socket.on('response', (data) => {
            console.log('Received response:', data);
        });

        socket.on('error', (error) => {
            console.error('Socket error:', error);
        });

        return () => {
            socket.off('connect');
            socket.off('response');
            socket.off('error');
            socket.close();
        };
    }, []);

    return socket;
}

export default useSocket;