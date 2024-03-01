import Header from "./components/header"
import Login from "./pages/login"
import {Outlet} from 'react-router-dom'

function App() {
  return (
    <div style={{height:"100vh", width:"100%"}}>
      <Header/>
      <Outlet/>
    </div>
  )
}

export default App
