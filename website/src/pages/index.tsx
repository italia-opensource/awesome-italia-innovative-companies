import React from 'react';
import Layout from '@theme/Layout';
import TableFeatures from '@site/src/components/TableFeatures';
import NewsletterForm from '@site/src/components/NewsletterForm';


export default function Home(): JSX.Element {
  return (
    <Layout
      title={`Home`}
      wrapperClassName="layout"
      description="Awesome Italia Startups is a list of italian startups. The repository intends to give visibility to startups and stimulate the community to contribute to growing the ecosystem.">
      <main className="main">
        

        <section className="wrapper">
        <div className="content">

        <header>
              <h1>Awesome Italia Startups</h1>
            </header>
            <section>
              <p>
                Awesome Italia Startups is a list of italian startups.<br/> 
                The repository intends to give visibility to startups and stimulate the community to contribute to growing the ecosystem.
              </p>
              <TableFeatures />
            </section>
          </div>
        </section>


        <section className="wrapper">
          <div className="content">
            <header>
              <h1>About Project</h1>
            </header>
            <section>
              <h3>
              The "Italia Opensource" project is the first of a series, the idea is to be able to give visibility to the Italian tech ecosystem, I started from what I know best: Software.
               </h3>
              <h3>
              This is a starting point, the goal is to be able to create an open community that can collaborate on projects and events until we get to have an ecosystem based on open source.
               </h3>
              <p>
                - Fabrizio Cafolla
               </p>
            </section>
          </div>
        </section>

        <section className="wrapper">
          <div className="content">
            <header>
              <h1>Subscribe Us</h1>
            </header>
            <section>
              <p>
              The newsletter will be dedicated to keeping you updated on new open source projects, new startups in the Italian community and events around the country.
              </p>
            </section>
            <footer>
              <NewsletterForm />
            </footer>
          </div>
        </section>
      </main>
    </Layout>
  );
}