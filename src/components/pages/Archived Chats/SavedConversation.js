import React, { useEffect, useState } from 'react';
import './SavedConversation.css';
import backgroundImage from '../../../images/archived-chats.jpg';
import Footer from '../../Footer';

const SavedConversation = () => {
    const [conversations, setConversations] = useState([]);
    const [searchTerm, setSearchTerm] = useState('');
    const [favorites, setFavorites] = useState([]);
    const [showFavorites, setShowFavorites] = useState(false);

    useEffect(() => {
        const fetchConversations = async () => {
            try {
                const response = await fetch('http://localhost:5000/api/conversations/1', {
                    credentials: 'include'  // Include cookies with the request
                });
                const data = await response.json();
                setConversations(data);
            } catch (error) {
                console.error('Failed to fetch conversations:', error);
            }
        };
        fetchConversations();
    }, []);
    
    const viewConversation = (title) => {
        alert('Viewing conversation: ' + title);
    };

    const deleteConversation = async (id) => {
        try {
            const response = await fetch(`http://localhost:5000/api/conversations/delete/${id}`, {
                method: 'DELETE',
                credentials: 'include'  // Include cookies with the request
            });
            if (response.ok) {
                setConversations(conversations.filter(conversation => conversation.id !== id));
            } else {
                console.error('Failed to delete the conversation');
            }
        } catch (error) {
            console.error('Error deleting conversation:', error);
        }
    };
    

    const toggleFavorite = async (id) => {
        try {
            const response = await fetch(`http://localhost:5000/api/conversations/toggle_favorite/${id}`, {
                method: 'POST',
                credentials: 'include'  // Include cookies with the request
            });
            if (response.ok) {
                if (favorites.includes(id)) {
                    setFavorites(favorites.filter(fav => fav !== id));
                } else {
                    setFavorites([...favorites, id]);
                }
            } else {
                console.error('Failed to toggle favorite');
            }
        } catch (error) {
            console.error('Error toggling favorite:', error);
        }
    };
    

    const handleSearch = (event) => {
        setSearchTerm(event.target.value);
    };

    const filteredConversations = conversations.filter(conversation =>
        conversation.title.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const displayedConversations = showFavorites
        ? filteredConversations.filter(conversation => favorites.includes(conversation.id))
        : filteredConversations;

    const backgroundImageStyle = {
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        minHeight: '100vh',
        padding: '20px'
    };

    return (
        <div>
            <div style={backgroundImageStyle}>
                <header>
                    <h1>Archived Chats</h1>
                </header>
                <div className="container">
                    <input
                        type="text"
                        placeholder="Search conversations..."
                        value={searchTerm}
                        onChange={handleSearch}
                        className="search-bar"
                    />
                    <button
                        className="toggle-favorites-button"
                        onClick={() => setShowFavorites(!showFavorites)}
                    >
                        {showFavorites ? 'Show All Conversations' : 'Show Favorites Only'}
                    </button>
                    <div className="conversation-list">
                        {displayedConversations.map(conversation => (
                            <div key={conversation.id} className="conversation-item">
                                <h3>{conversation.title}</h3>
                                <p className="conversation-date">{conversation.date}</p>
                                <p>{conversation.snippet}</p>
                                <div className="actions">
                                    <button className="view-button" onClick={() => viewConversation(conversation.title)}>View Full Conversation</button>
                                    <button className="delete-button" onClick={() => deleteConversation(conversation.id)}>Delete</button>
                                    <button
                                        className="favorite-button"
                                        onClick={() => toggleFavorite(conversation.id)}
                                        style={{ background: favorites.includes(conversation.id) ? 'gold' : '#0779e4' }}
                                    >
                                        {favorites.includes(conversation.id) ? 'Unfavorite' : 'Favorite'}
                                    </button>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
            <Footer />
        </div>
    );
};

export default SavedConversation;
