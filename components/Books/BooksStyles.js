//TODO checkout https://github.com/TimMartin13-Frontend-Mentor/product-preview-card-component/blob/main/src/components/ProductCard/styles.js

// Import styled-components library - "import" version
import styled from 'styled-components'
import { css } from 'styled-components'

// Helper function to convert pixels to rems (remy)
const remy = px => `${px / 16}rem`

// Function for calculating value for width
const getWidth = (value) => {
  if (!value) return

  let width = value / 12 * 100
  return `width: ${width}%;`
}

// Function for calculating value for flex
const getFlex = (value) => {
  if (!value) return

  let flex = value / 12 * 100
  return `flex: 0 0 ${flex}%;`
}

// Grid container
export const GridContainer = styled.div`
  padding-right: ${remy(15)};
  padding-left: ${remy(15)};
  margin-right: auto;
  margin-left: auto;
  width: 100%;

  // Breakpoint for tablets
  @media (min-width: 576px) {
    max-width: ${remy(540)};
  }

  // Breakpoint for small desktops
  @media (min-width: 768px) {
    max-width: ${remy(720)};
  }

  // Breakpoint for medium desktops
  @media (min-width: 992px) {
    max-width: ${remy(9600)};
  }

  // Breakpoint for large desktops and HD devices
  @media (min-width: 1200px) {
    max-width: ${remy(1140)};
  }
`

// Grid row
export const GridRow = styled.div`
  margin-right: ${remy(-15)};
  margin-left: ${remy(-15)};
  display: flex;
  flex-wrap: wrap;
`

// Grid columns
export const GridColumn = styled.div`
  padding-right: ${remy(15)};
  padding-left: ${remy(15)};

  // Columns for mobile
  ${({ xs }) => (xs ? getFlex(xs) : 'flex: 0 0 100%')};
  ${({ xs }) => (xs ? getWidth(xs) : 'width: 100%')};

  // Columns for tablets
  @media (min-width: 576px) {
    ${({ sm }) => sm && getFlex(sm)};
    ${({ sm }) => sm && getWidth(sm)};
  }

  // Columns for small desktops
  @media (min-width: 768px) {
    ${({ md }) => md && getFlex(md)};
    ${({ md }) => md && getWidth(md)};
  }

  // Columns for medium desktops
  @media (min-width: 992px) {
    ${({ lg }) => lg && getFlex(lg)};
    ${({ lg }) => lg && getWidth(lg)};
  }

  // Columns for large desktops and HD devices
  @media (min-width: 1200px) {
    ${({ xl }) => xl && getFlex(xl)};
    ${({ xl }) => xl && getWidth(xl)};
  }
`

export const Card = styled.article`
  position: relative;
  width: 100%;
  min-height: ${remy(380)};
  cursor: pointer;
  perspective: 1000px;
  transition: all .25s ease-in-out;

  &:focus,
  &:hover {
    box-shadow: 0 0 ${remy(40)} rgba(0,0,0,.15);
  }

  &.flipped {
    & > div:first-of-type { // frontside of the card
      transform: perspective(1000px) rotateY(-180deg);
    }

    & > div:last-of-type { // backside of the card
      transform: perspective(1000px) rotateY(0deg);
    }
  }
`

// Card sides
const CardSide = css`
  position: absolute;
  top: 0;
  left: 0;
  overflow: hidden;
  padding: ${remy(24)};
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  transition: all .25s ease-in-out;
`

// Card side - front
export const CardFront = styled.div`
  ${CardSide};

  font-weight: bold;
  text-align: center;
`

// Card side - back
export const CardBack = styled.div`
  ${CardSide};

  transform: rotateY(-180deg);
`

// Card content
export const CardNumber = styled.span`
  display: block;
  font-size: ${remy(24)};
`

export const CardTitle = styled.h2`
  font-size: ${remy(21)};
`

export const CardDescription = styled.span`
  font-size: ${remy(16)};
`