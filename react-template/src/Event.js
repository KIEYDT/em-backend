import React, { useEffect, useState } from "react";
import { createEvent, createInviteLink, getEventById, getEventByUser, getInviteLink } from "./api";
import { useLocation, useNavigate } from "react-router-dom";
import './Event.css';


function ViewEvent() {
    const [user, setUser] = useState([])
    const [events, setEvents] = useState([])
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                const events = await getEventByUser();
                setEvents(events);
                
            } catch (error) {
                
                throw error;
            }
        }

        fetchData();
    }, []);

    const handleCreateEvent = async (e) => {
        e.preventDefault();
        navigate("/create");
    }

    const handleClickEvent = (data) => {
        navigate("/event", { 
            state: { eventData: data }, 
        });
    }

    const DEBUGClickEvent = (data) => {
        
    }

    return (
        <div>
            <div>
                <span>Event</span>
                <ul>
                    {events.map((event) => (
                        <li key={event.id}>
                            <div>
                                <span className="redirect" onClick={() => handleClickEvent(event)}>{event.title}</span>
                            </div>
                        </li>
                    ))}
                </ul>
                <button onClick={handleCreateEvent}>
                    <span>Create Event</span>
                </button>
            </div>
        </div>
    );
}

function CreateEvent() {
    const [formData, setFormData] = useState({
        title: "",
        description: "",
        price: "",
        capacity: "",
        approval: false,
    })
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData({
            ...formData,
            [name]: type === "checkbox" ? checked : value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await createEvent(formData);
            if (response) {
                alert("POST data");
                navigate("/home");
            }
        } catch (err) {
            throw err;
        } 
    };

    return (
        <div>
            <span>Create Event</span>
            <form onSubmit={ handleSubmit }>
                <div>
                    <span>Event Name</span>
                    <input
                        type="text"
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <span>Description</span>
                    <textarea
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <span>Price</span>
                    <input
                        type="number"
                        name="price"
                        value={formData.price}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <span>Capacity</span>
                    <input
                        type="number"
                        name="capacity"
                        value={formData.capacity}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div>
                    <span>Approval</span>
                    <input
                        type="checkbox"
                        name="approval"
                        value={formData.approval}
                        onChange={handleChange}
                    />
                </div>
                <button type="submit">Create</button>
            </form>
        </div>
    )
};

// function RegisterModal() {
//     const [questions, setQuestions] = useState([]);
//     const [answers, setAnswers] = useState([]);
// }

function RegisterEvent() {
    const navigate = useNavigate();
    const location = useLocation();
    const [event, setEvent] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false)
    const { eventData } = location.state || {};
    
    useEffect(() => {
        const fetchData = async () => {
            try {
                setEvent(eventData);
                
                
            } catch (error) {
                
                throw error;
            }
        }
        fetchData();
    }, [setEvent]);

    const handleRegister = (e, id) => {
        e.preventDefault();
        navigate("/RegisterForm", {
            state: {
                eventId: id,
            }
        });
    }

    return (
        <div className="container">
            <div>
                <h1>{event.title}</h1>
            </div>
            <div>
                <p>{event.description || <p>No Description Yet</p>}</p>
                <p>{event.price > 0 ? `${event.price} baht` : "free"}</p>
                <p>{event.approval ? "approval required" : "no approval"}</p>
                <p>{event.capacity > -1 ? `${event.capacity}` : "Unlimited"}</p>
            </div>
            <div>
                <button onClick={() => handleRegister(event.id)}>
                    Register
                </button>
            </div>
            {/* <RegisterForm
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
            /> */}
        </div>
    )
};

function Event() {
    const location = useLocation();
    const [event, setEvent] = useState({});
    const [inviteLink, setInviteLink] = useState("");
    const { eventData } = location.state || {};

    useEffect(() => {
        const fetchData = async () => {
            try {
                // const response = await getInviteLink(eventData.id);
                // if (response) {
                //     setInviteLink(response.data);
                //     
                // } else {
                //     setInviteLink("127.0.0.1:8000/home");
                //     
                // }
                setEvent(eventData);
                
                
            } catch (error) {
                
                throw error;
            }
        }
        fetchData();
    }, [setEvent]);

    // FIXME: implement generate link
    const handleGenerateInviteLink = async (e, id) => {
        e.preventDefault();
        const response = await createInviteLink(id);
        if (response) {
            setInviteLink(response.data);
            
        } else {
            
        }
    };

    return (
        <div className="container">
            <div>
                <h1>{event.title}</h1>
            </div>
            <div>
                <p>{event.description || <p>No Description Yet</p>}</p>
                <p>{event.price > 0 ? `${event.price} baht` : "free"}</p>
                <p>{event.approval ? "approval required" : "no approval"}</p>
                <p>{event.capacity > -1 ? `${event.capacity}` : "Unlimited"}</p>
            </div>
            <div>
                {/* <button onClick={() => handleGenerateInviteLink(event.id)}>Generate invite link</button> */}
                <button value={inviteLink}></button>
            </div>
        </div>
    )
}


export { ViewEvent, CreateEvent, Event };