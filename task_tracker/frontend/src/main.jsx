import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import { AuthState } from './states/authState.jsx'
import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import Home from './pages/home/index.jsx'
import Login from './pages/login/index.jsx'

const router = createBrowserRouter([
  {
    path: "/",
    element: <App/>,
    children:[
      {
        path:"",
        element:<Home/>
      },
      {
        path:"login",
        element:<Login/>
      }
    ]
  }  
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <AuthState>
    <React.StrictMode>
      <RouterProvider router={router}/>
    </React.StrictMode>,
  </AuthState>
)
