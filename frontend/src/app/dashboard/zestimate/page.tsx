"use client";
import { Box, Button, Snackbar, TextField } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import Image from 'next/image'
import {BRIDGE_KEY} from '../config'

async function ZestimateRetriever(address: string) {
  console.log('call')
  const docs = await fetch(`https://api.bridgedataoutput.com/api/v2/zestimates_v2/zestimates?access_token=${BRIDGE_KEY}&address=${address}`, {
    method: 'GET',
        headers: {

        }
    })
    const data = await docs.json()
    try{
        return data.bundle[0]?.zestimate
    } catch{
        console.log('caught')
    }
}

export default function Home() {
  const router = useRouter();
  const [value, setValue] = useState("");
  return (
    <>
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
        <TextField
          label="Zestimate Retriever"
          id='address'
          helperText="Type in an address"
          color="secondary"
          focused
        />
        <Button sx={{mt:2, mb:2}} variant="text" onClick={async () => {
            setValue(await ZestimateRetriever((document.getElementById('address') as HTMLInputElement)?.value));
        }}> Get Zestimate</Button>
        {value && <Button size='large' variant="outlined" startIcon={<Image src="/ZillowLogo.png" width={25} height={25} alt={"Zestimate Image"}/>}>${value}</Button>}
      </Box>
    </>
  );
}
