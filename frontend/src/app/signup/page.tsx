"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import AuthForm from "@/components/auth-form";
import { signUp } from "@/lib/auth-client";

export default function SignUpPage() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);

  async function handleSignUp(data: {
    name?: string;
    email: string;
    password: string;
  }) {
    setError(null);
    const { error: authError } = await signUp.email({
      name: data.name || "",
      email: data.email,
      password: data.password,
    });

    if (authError) {
      if (authError.message?.toLowerCase().includes("already")) {
        setError("An account with this email already exists.");
      } else {
        setError(authError.message || "Signup failed. Please try again.");
      }
      return;
    }

    router.push("/dashboard");
    router.refresh();
  }

  return (
    <main className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-md">
        <AuthForm mode="signup" onSubmit={handleSignUp} error={error} />
        <p className="mt-4 text-center text-sm text-gray-600">
          Already have an account?{" "}
          <Link href="/signin" className="text-blue-600 hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </main>
  );
}
