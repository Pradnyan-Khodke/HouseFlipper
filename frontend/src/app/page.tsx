'use client'
import { useSession } from 'next-auth/react'
import LoginPage from './auth/login/page'
import Dashboard from "./dashboard/page"
import Stack from '@mui/material/Stack';
import CircularProgress from '@mui/material/CircularProgress';

export default function Home() {
  const session = useSession();
  if(session.status === "unauthenticated"){
    return(<LoginPage/>)
  } 
  if(session.status === "loading"){
    return(
      <Stack display="flex" justifyContent="center" alignItems="center" minHeight="100vh" direction="row" spacing={5}>
        <CircularProgress color="primary" size={100}/>
        <CircularProgress color="primary" size={100}/>
        <CircularProgress color="primary" size={100}/>
      </Stack>
    )
  }
  if(session.status === "authenticated"){
    return(
      <Dashboard/>
    )
  }
}
