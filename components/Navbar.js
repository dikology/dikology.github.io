import React, { useEffect, useState } from 'react';
import Link from 'next/link';

import { AiFillGithub, AiFillInstagram, AiFillLinkedin } from 'react-icons/ai'
import { DiCssdeck } from 'react-icons/di'
import { FaTelegramPlane } from 'react-icons/fa'

import { Container, Div1, Div2, Div3, NavLink, SocialIcons, Span } from './NavStyles'

const Nav = () => (
  <Container>
    <Div1>
      <Link href="/">
        <a style={{display: "flex", alignItems: "center", color:'white', marginBottom:'20px'}}>
          <DiCssdeck size="3rem" /> <Span>Dikology</Span>
        </a>
      </Link>
    </Div1>
    <Div2>
      <li>
        <Link href="#projects">
          <NavLink>Projects</NavLink>
        </Link>
      </li>
      <li>
        <Link href="#tech">
          <NavLink>What I do</NavLink>
        </Link>
      </li>
      <li>
        <Link href="#about">
          <NavLink>About</NavLink>
        </Link>
      </li>
    </Div2>
    <Div3>
    <SocialIcons href="https://t.me/dikobrist">
        <FaTelegramPlane size="3rem" />
      </SocialIcons>
      <SocialIcons href="https://github.com/dikology">
        <AiFillGithub size="3rem" />
      </SocialIcons>
      <SocialIcons href="https://linkedin.com/in/dikology">
        <AiFillLinkedin size="3rem" />
      </SocialIcons>
      <SocialIcons href="https://instagram.com/unpotato_lifestyle">
        <AiFillInstagram size="3rem" />
      </SocialIcons>
    </Div3>
  </Container>
)

export default Nav