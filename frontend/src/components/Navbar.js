import React from 'react'
import { Link } from 'react-router-dom'

export const Navbar = () => (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container"  >
            <Link className="navbar-brand" to="/">CRUD POKEMON DATA</Link>
        </div>
    </nav>
)