"use client";
import { Avatar, Box, Button, Card, CardActions, CardContent, CircularProgress, Container, Divider, Stack, Typography } from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import { Copyright } from "@mui/icons-material";
import Image from 'next/image'
import React from "react";

interface MainTextMatchedSubstrings {
  offset: number;
  length: number;
}
interface StructuredFormatting {
  main_text: string;
  secondary_text: string;
  main_text_matched_substrings?: readonly MainTextMatchedSubstrings[];
}
interface PlaceType {
  description: string;
  structured_formatting: StructuredFormatting;
}

type Props = {
  children: JSX.Element;
  waitBeforeShow?: number;
}

const Delayed = ({children, waitBeforeShow = 500}: Props) => {
  const [isShown, setIsShown] = useState(false);

  useEffect(()=>{
    const timer = setTimeout(()=>{
      setIsShown(true)
    }, waitBeforeShow)
    return () => clearTimeout(timer);
  }), [waitBeforeShow]

  return isShown ? children : null
}


export default function Home() {
  const router = useRouter();
  const [response, setResponse] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  useEffect(() => {
    async function getMarket(){
      setIsLoading(true)
      let value: PlaceType | null = JSON.parse(
        window?.localStorage.getItem("Address") ?? "{}"
      );
      if (JSON.stringify(value) === '{}') {
        router.push("/dashboard/flipper");
      }
      const full_array = value?.description.split(',')
      if(value?.description && full_array?.length == 4){
        value.description = full_array[0] + ',' + full_array[2]
      } else if(value?.description && full_array?.length == 3){
        value.description = full_array[0] + ',' + full_array[1]
      }
      const docs = await fetch('http://127.0.0.1:5000', {
      method: 'GET',
          headers: {
            'location': value?.description ?? "Cody, WY"
          }
      })
      const data = await docs.json()
      if(data){
        data.sort((a: { [x: string]: number; }, b: { [x: string]: number; }) => b['POTENTIAL PROFIT'] - a["POTENTIAL PROFIT"])
        localStorage.setItem('market-data', JSON.stringify(data))
      }
      console.log(data)
      setResponse(data)
      setIsLoading(false)
    }
    if(response.length == 0 && typeof window !== 'undefined'){
      setIsLoading(true)
      const response = JSON.parse(window.localStorage.getItem('market-data') ?? '{}')
      if(JSON.stringify(response) != '{}'){
        setResponse(response)
        setIsLoading(false)
      } else {
        getMarket()
      }
    }
  }, [])
  return (
    <>
      <Button
        startIcon={<ArrowBackIcon />}
        onClick={() => router.push("/dashboard/flipper")}
      >
        City Selection
      </Button>
      <Button
        endIcon={<ArrowForwardIcon />}
        onClick={() => router.push("/dashboard")}
        style={{ float: "right" }}
      >
        Dashboard
      </Button>
      <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
      flexDirection='row'
      flexWrap='wrap'
      >
        {
          isLoading && 
            <Stack display="flex" justifyContent="center" alignItems="center" minHeight="100vh" direction="row" spacing={5}>
              <CircularProgress color="secondary" size={100}/>
            </Stack>
        }
        {
          !isLoading && response.length !== 0 ? 
          response.map((dataResponse) => {
            return(
              <Box key={dataResponse["ADDRESS"]} sx={{ minWidth: 275, maxWidth: 500, ml:2, mr:2, mt:2, mb:2 }}>
                <Card variant="outlined">
                  <React.Fragment>
                    <CardContent>
                      <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                        {dataResponse["PROPERTY TYPE"]}
                      </Typography>
                      <Typography variant="h5" component="div">
                        {dataResponse["ADDRESS"]}
                      </Typography>
                      <Typography sx={{ mb: 1.5 }} color="text.secondary">
                        Price {dataResponse["PRICE"]}
                      </Typography>
                      <Typography variant="body2">
                        Zestimate: {dataResponse["ZESTIMATE"] == 0 ? 'No Zestimate Found' : dataResponse["ZESTIMATE"] }
                        <br />
                        Predicted Price: {dataResponse["PREDICTED PRICE"] == 0 ? 'Could not calculate predicted price' : dataResponse['PREDICTED PRICE']}
                        <br />
                        Potential Profit: {dataResponse['POTENTIAL PROFIT'] == 0 ? 'Could not calculate profit' : dataResponse['POTENTIAL PROFIT']}
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button size="small" href={dataResponse["URL"]}>Learn More</Button>
                    </CardActions>
                  </React.Fragment>
                </Card>
              </Box>
            )
          })
        :
        <Delayed>
           <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            minHeight="100vh"
            flexDirection='column'
          >
            <Button style={{display: !isLoading ? "" :"none"}} color='secondary' size='large' >No Data Found</Button>
          </Box>
        </Delayed>
        }

      </Box>
    </>
  );
}
