import axios from "axios";

const API = axios.create({
    baseURL: "/api",
})

// not using
export const signin = async (email, password) => {
    try {
        const response = await API.post("/signin/", { email, password });
        const { access, refresh } = response.data;
        localStorage.setItem("access", access);
        localStorage.setItem("refresh", refresh);
        return access;
    } catch (error) {
        throw error;
    }
};

export const refreshAccessToken = async () => {
    try {
        const refreshToken = localStorage.getItem("refresh");
        const response = await API.post("/refresh/", { refresh: refreshToken });
        const { access } = response.data;

        localStorage.setItem("access", access);

        return access;
    } catch (error) {
        throw error;
    }
};

API.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem("access");
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export const getProfile = async () => {
    try {
        const response = await API.get("/user/", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

export const getEventByUser = async () => {
    try {
        const response = await API.get("/event/", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
        },);
        return response.data;
    } catch (error) {
        throw error;
    }
}

export const getEventById = async (id) => {
    try {
        const response = await API.get("/event/", id);
        return response.data;
    } catch (error) {
        
        throw error;
    }
};

export const createEvent = async (data) => {
    try {
        const response = await API.post("/event/", data, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
         });
         
         return response.data;
    } catch (error) {
        
        throw error;
    }
};

export const getTicket = async (id) => {
    try {
        const response = await API.get("/ticket/", id);
        return response.data;
    } catch (error) {
        
        throw error;
    }
};

export const getQuestion = async (id) => {
    try {
        const response = await API.get("/question/", id);
        return response.data;
    } catch (error) {
        
        throw error;
    }
};

export const createQuestion = async (data) => {
    try {
        const response = await API.post("/question/add/", data, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
        });
        return response.data;
    } catch (error) {
        
        throw error;
    }
};

export const getAnswer = async (event_id) => {
    try {
        const response = await API.get("/answer/", event_id, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
        });
        return response.data;
    } catch (error) {
        
        throw error;
    }
};

export const submitAnswer = async (data) => {
    try {
        const response = await API.post("/answer/submit/", data)
        return response;
    } catch (error) {
        
        throw error;
    }
};

export const createInviteLink = async (id) => {
    try {
        const response = await API.post("/invite/create", id, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access")}`,
            },
        });
        return response;
    } catch (error) {
        
        throw error;
    }
};

export const getInviteLink = async (id) => {
    try {
        const response = await API.get("/invite/", id);
        return response.data;
    } catch (error) {
        
        return error;
    }
};