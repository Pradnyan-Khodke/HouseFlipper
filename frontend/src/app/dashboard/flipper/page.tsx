"use client";
import { Box, Button, Snackbar, TextField } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Image from 'next/image'
import SearchBox from "../components/SearchBox";

export default function Home() {
  const router = useRouter();
  const [value, setValue] = useState("");
  if(typeof window !== 'undefined'){
    localStorage.removeItem('Address')
    localStorage.removeItem('market-data')
  }
  return (
    <body style={{overflowY: "hidden", height: "100%"}}>
      <Button 
        startIcon={<ArrowBackIcon />}
        onClick={() => router.push("/dashboard")}
      >
        Dashboard
      </Button>
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="100vh"
        flexDirection='column'
      >
        <Button sx={{pb:3}} variant="text" size="large">
          To view a specific market, select a city located in the United States
        </Button>
        <SearchBox/>
      </Box>
    </body>
  );
}
