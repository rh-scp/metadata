# Package Metadata Description

## 1. Abstract
Working with many differing artifacts coming out of many differing package ecosystems requires us to find common ground between all
the ecosystems. While *requires* may have been a little strong wording to start with, let's overview the benefits of having
a common metadata description for all ecosystems:

 * Metadata storage - Database
   * All data are stored in generic rows
   * There' onlys one main table
   * Database can operate with the metadata directly
 * Common codebase
   * One API, one Interchange format
   * One binding for all client languages
 * Upstreams can change their metadata format on a whim

While some points are important during development, especially the last bullet is very important for long term maintenance, since it 
allows us to `contain` the volatile upstream specification within single minimal component for each ecosystem. Let's see an example:

```
         +-------------------+
IN       |                   |  OUT
         |  npm metadata     |
+------->+  manifest tool    +------------>
         |                   |
         +-------------------+
```

`IN`put is a `npm` package and `OUT`put is a document in common metadata format. Whenever the `npm` upstream changes its package specification
we only need to update this single component. The rest of the infrastructure is completely oblivious to the changes because it already
consumes the common metadata format.

Furthermore, taking a service oriented architecture into the picture, the crucial aspect of properly decoupled
services is *the means* how the services talk to each other, how they communicate, be it either the APIs or the underlying data interchange format.

## 2. Expressivity and flexibility

The language of the common metadata format shall be expressive enough so that we can always express a feature of one package format in terms
of the common metadata format. Expressivity can be thought of as the degree of *freedom* or *possibilities* that is needed to describe the particular
metadata component. Let's illustrate this on versioned dependencies - while some package ecosystem can do fine with rather simplistic rules for dependency versioning:

  * `>= 1.0.0`
  * `1.0.0`
  * `>= 1.2`
  
There also exist much *more complex* dependency variants:

  * `[1.2.0, 1.3.5],(1.4.2,]`
  * `1.0 <= 1.4.5`
  
In other words, we'll always need to pick the definition with strongest expressivity, that is, the superset of all features.
If we ever come to need to amend the needed expressivity we can do so by bumping the version of the common metadata format and updating the baseline API, which also localizes
the changes needed to perform on the system to a *single component*. The flexibility comes from the fact that globally, our system does not really care that we changed the expressivity of one component
because all the changes were made within the particular component (we should only ever need to *increase* the expressivity).

## 3. Common Metadata Interchange Format

While the database storage format can be different for each kind of database backend that we can think of, the more chiseled in stone the *data interchange* format, the better.
The common metadata interchange format will be the *lingua franca* of the entire system, and according to the strong Sapir-Whorf hypothesis on linguistic relativity: 
> "... the linguistic categories limit and determine cognitive categories ..."

In the world of programming and mathematics, this nicely translates to the concept of pure function, where the output of the function is consistently determined *only* from the inputs and without any observable side-effects.
That being said, what we put into the metadata will limit and determine how the metadata is processed and consumed.

### 3.1 Format Proposal

JSON document with enforced schema validation. This has been used to a great success in Nulecule already, so let's build on top of that.
Concrete definitions are beyond the scope of this document, and are described in these linked documents:

  * Common Metadata Interchange Format
    * Manifest description
    * Component description
  * Common Metadata Interchange Format - Schema
