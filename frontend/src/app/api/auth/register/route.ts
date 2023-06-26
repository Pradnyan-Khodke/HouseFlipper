import User from "@/models/User";
import {connectToDb} from "@/utils/db"
import { NextResponse } from "next/server";
import bcrypt from "bcryptjs";

export const POST = async (request: any) => {
    const {first_name, last_name, email, password} = await request.json();
    await connectToDb();
    const hashedPassword = await bcrypt.hash(password, 5)
    const newUser = new User({
        first_name, 
        last_name,
        email,
        password: hashedPassword,
    });        

    try{
        console.log('reached')
        await newUser.save()
        return new NextResponse("User has been created", {
            status: 201, 
        })
    } catch(err: any) {
        return new NextResponse(err.message, {
            status: 500,
        });
    }
}