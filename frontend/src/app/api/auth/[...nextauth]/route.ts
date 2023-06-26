import NextAuth from "next-auth"
import GoogleProvider from "next-auth/providers/google"
import CredentialProvider from "next-auth/providers/credentials"
import { connectToDb } from "@/utils/db";
import User from "@/models/User";
import bcrypt from "bcryptjs";

const handler = NextAuth({
    providers: [
        GoogleProvider({
            clientId: process.env.GOOGLE_CLIENT_ID,
            clientSecret: process.env.GOOGLE_CLIENT_SECRET,
        }),
        CredentialProvider({
            id: "credentials",
            name: "Credentials",
            async authorize(credentials) {
                await connectToDb();
                try {
                    const user = await User.findOne({
                        email: credentials.email,
                    });
                    if (user) {
                        const isPasswordCorrect = await bcrypt.compare(
                            credentials.password,
                            user.password
                        ); if (isPasswordCorrect) {
                            return user;
                        }
                        else {
                            throw new Error("Wrong Credentials!");
                        }
                    } else {
                        throw new Error("User not found!");
                    }
                } catch (err: any | undefined) {
                    throw new Error(err);
                }
            },
            credentials: undefined
        }),
    ],
    pages:{
        error: "/"
    }
})
  
export { handler as GET, handler as POST }