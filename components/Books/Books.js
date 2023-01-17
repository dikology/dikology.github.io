import React from 'react';

import { GridRow, GridColumn, Card, CardFront, GridContainer, CardNumber, CardTitle, CardBack, CardDescription, TitleContent, UtilityList, Img } from './BooksStyles';
import { Section, SectionDivider, SectionTitle } from '../../styles/GlobalComponents';
import { books } from '../../constants/constants';

const Projects = () => (
  <Section nopadding id="books">
    <SectionDivider />
    <SectionTitle main>Books I read</SectionTitle>
        <GridContainer>
          <GridRow>
            <GridColumn sm='6' lg='4'>
              <Card >
                <CardFront>
                  <CardNumber>1.</CardNumber>

                  <CardTitle>Card</CardTitle>
                </CardFront>

                <CardBack>
                  <CardDescription>Rand's stated goal for writing the novel was "to show how desperately the world needs prime movers and how viciously it treats them" and to portray "what happens to the world without them".</CardDescription>
                </CardBack>
              </Card>
            </GridColumn>

            <GridColumn sm='6' lg='4'>
              <Card >
                <CardFront>
                  <CardNumber>2.</CardNumber>

                  <CardTitle>Card</CardTitle>
                </CardFront>

                <CardBack>
                  <CardDescription>The core idea for the book came to her after a 1943 telephone conversation with a friend, who asserted that Rand owed it to her readers to write fiction about her philosophy.</CardDescription>
                </CardBack>
              </Card>
            </GridColumn>

            <GridColumn sm='6' lg='4'>
              <Card >
                <CardFront>
                  <CardNumber>3.</CardNumber>

                  <CardTitle>Card</CardTitle>
                </CardFront>

                <CardBack>
                  <CardDescription>To produce Atlas Shrugged, Rand conducted research on the American railroad industry. Her previous work on a proposed (but never realized) screenplay.</CardDescription>
                </CardBack>
              </Card>
            </GridColumn>

            <GridColumn sm='6' lg='4'>
              <Card >
                <CardFront>
                  <CardNumber>4.</CardNumber>

                  <CardTitle>Card</CardTitle>
                </CardFront>

                <CardBack>
                  <CardDescription>Atlas Shrugged is set in a dystopian United States at an unspecified time, in which the country has a "National Legislature" instead of Congress and a "Head of State" instead of a President.</CardDescription>
                </CardBack>
              </Card>
            </GridColumn>
          </GridRow>
        </GridContainer>
  </Section>
);

export default Projects;