https://lucid.app/lucidchart/deefdde8-04dc-48bc-80cf-ac5ae84839af/edit?invitationId=inv_ceb2d465-a29a-4105-a2df-67671c059900&page=HWEp-vi-RSFO#

# Introduction
- Low Level Design is to design at the component level.  It includes creating classes and methods.
- This is how classes and interfaces are represented.
![class_interface.png](images/class_interface.png)
- Abstract Class vs Interface:

# OOPS Concepts
- objects
- classes
- Inheritance
- Encapsulation
- Abstraction
- Polymorphism: runtime, compile time, method overloading, method overriding

# SOLID Principles


# Relationship between classes
- Association:
  - This defines a **call** relationship.  For example, if A has an association with B, then A can call B (but B may or may not call A).
  - Types:
    - Bidirectional: 
      - Class A can call B and vice versa.  
      - For example, Guide class can call Hiker class and vice versa.
      - It is represented using a line without any arrows
    - Unidirectional: 
      - Class A can call B but B cannot call A.  
      - For example, Guide class can call Trail class, but Trail class cannot call Guide class. 
      - It is denoted using a line with an arrow from the caller to the callee class.
      - ![association.png](images/association.png)
  - Multiplicity:
    - It denotes the number of instances of a class that can be associated with a different class.
    - We write the number of instances at the arrow end-points.
    - How to write a number:
      - n denotes n number of instances
      - x..y denotes a minimum of x and a maximum of y instances.  Ex: 1..5
      - * denotes any number of instances
    - ![num_instances.png](images/num_instances.png)
  - Sometimes the name of th relationship is written in the arrow to denote how a class is associated with other classes.  For example, A Guide guides a hiker, and follows a trail.
    - ![relationship_name.png](images/relationship_name.png)
- Aggregation:
  - Aggregation and Composition comes under **has-a** relationship.
  - Class A **has-a** class B instance, but a class B instance can exist without class A.  For example, a HikeEvent **has-a** Trail, but a Trail can exist without a HikeEvent.
  - It is denoted using a diamond arrow.
  - If a class can be a part of multiple classes, then it cannot be a composition relationship.  It has to be aggregation.  Ex: a Trail class can belong to a HikingEvent, a Guide, a Hiker etc.
- Composition:
  - A class B cannot exist without A.  For example, a License cannot exist without a Guide.  A Guide **has-a** License.
  - In this case, we should delete class B whenever we delete class A.
  - Therefore, sometimes it is also called **part-of** relationship.
  - It is denoted using a diamond arrow, but the diamond is colored.
- Inheritance:
  - **is-a** relationship.
  - ![aggregation_composition_inheritance.png](images/aggregation_composition_inheritance.png)
  - Abstract class or Interface: A **implements** B.  It is denoted using a dotted line.
    - To denote an interface just use the same class box as earlier, and mention the class name in italics.


# Design Patterns
- Strategy:
  - It is used when a class "has-a" another class and that class might change behaviour based on certain conditions.
  - For example, A Order class might have to pay() to complete the order.
    - Now, if we have different options of payment like Gpay, phonepay, etc. then we might have to subclass multiple Order classes like GpayOrder, PhonePayOrder etc. which will unnecessarily duplicate some of the common code of Order class.  Also, it breaks the DRY principle, and we might have to change multiple classes (GpayOrder, PhonePayOrder etc.) if we have to make just one change (breaks O prinicple of SOLID).
    - Solution: Order "has-a" interface Pay with pay() and Gpay, PhonePay etc. implements this interface.
      - Order is injected either Gpay or PhonePay and Order simply calls pay() provided by the interface.
- Singleton:
  - It is used when we want only one instance of a class.
  - Uses: to limit access to a heavily used resource like DB, logging, caching data, threadpool etc.
- Factory
  - It is used to create classes of similar family.  For example, different shapes like circle, triangle, rectangle can have the same function draw().
  - If we want to create these classes based on if-else conditions then, it will break the Open-Closed principle because to introduce a new class of family shape, we will have to modify the client class with a new if condition and the if-else nest might get confusing if there are 200 classes of that type for example.
  - Solution:
    - Create a base Factory class from which different Shape creator factory classes can implement.  These different shape creator factory classes are responsible to create different shape objects.
    - Create a base Shape class which functions common to all shapes.  Now, different shapes inherit from this class.
    - Now, from the calling client class, get the correct shape class using the correct factory-creator and use the functions from this.
- AbstractFactory
- Observer
  - It is used when multiple clients need to be updated in reaction to a state change in a class.  For example, if it starts raining then all clients need to be updated that their food delivery might be delayed.
  - All the observer client classes might subscribe and unsubscribe to the class with the state, and they need to implement an interface with notify()
- Decorator
  - It is used to stop explosion of classes.  For example, for pizza we can have a number of basePizzas (like margerita, veggie, onionPizza etc.) and number of toppings (like extrachesse, extraOnions, extraGarlic etc.).
  - Now if we want to provide clients with flexible selections then we need to create exponential number of classes:
    - with 0 extra topping - margherita, veggie etc.
    - with 1 extra topping - margheritaExtraCheese, margheritaExtraOnion, VeggieExtraCheese, VeggieExtraOnion etc.
    - with 2 extra toppings - margheritaExtraCheeeseExtraOnion, margheritaExtraCheeeseExtraGarlic, margheritaExtraGarlicExtraOnion, ...
    - Also if a new base pizza or topping is introduced we will have to add a lot of new classes.
  - Decorator helps with this problem by:
    - basePizza abstract class, from which concrete basePizza like Margherita inherits
    - toppingDecorator which is-a (inheritance) and has-a (composition) basePizza at the same time.
    - The is-a relationship forces the decorator to implement the ingredients() and pay() method for example.
- Builder
- Adapter
- Facade

# Other Concepts
- Sequence Diagrams
- Activity Diagrams
- Test Cases
- Multi-Threading: how is it implemented in Singleton Pattern?

# Examples
- Hotel Management System
- Car Parking System
- Elevator Management
- 2 player games like Chess, Tic Tac Toe
- Ticket Booking System
- ATM