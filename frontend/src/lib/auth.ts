import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  database: {
    type: "postgres",
    url: process.env.DATABASE_URL!,
  },
  plugins: [
    jwt(),
  ],
  secret: process.env.BETTER_AUTH_SECRET,
});
