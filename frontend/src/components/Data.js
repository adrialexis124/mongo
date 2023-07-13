import React, { useState, useEffect, useRef } from "react";

const API = process.env.REACT_APP_API;

export const Data = () => {
    const [name, setName] = useState("");
    const [height, setHeight] = useState("");
    const [weight, setWeight] = useState("");
    const [egg, setEgg] = useState("");

    const [editing, setEditing] = useState(false);
    const [id, setId] = useState("");

    const nameInput = useRef(null);

    let [data2, setData2] = useState([]);

    




    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!editing) {
            const res = await fetch(`${API}/api/data`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name,
                    height,
                    weight,
                    egg,
                    

                }),

            });
            await res.json();
            window.location.reload();


        } else {
            const res = await fetch(`${API}/api/data/${id.$oid}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    name,
                    height,
                    weight,
                    egg,
                }),
            });
            const data = await res.json();
            console.log(data);
            setEditing(false);
            setId("");

        }


        setName("");
        setHeight("");
        setWeight("");
        setEgg("");
        nameInput.current.focus();
        window.location.reload();
    };

    const getData2 = async () => {
        const res = await fetch(`${API}/api/data`);
        const data = await res.json();
        setData2(data);
    };

    const deleteDat = async (id) => {
        const userResponse = window.confirm("Are you sure you want to delete it?");
        if (userResponse) {
            console.log(id.$oid);
            const res = await fetch(`${API}/api/data/${id.$oid}`, {
                method: "DELETE",
            });
            const data = await res.json();
            console.log(data);
            await getData2();
        }
    };

    const editDat = async (id) => {
        const res = await fetch(`${API}/api/data/${id.$oid}`);
        const data = await res.json();

        setEditing(true);
        setId(id);

        // Reset
        setName(data.name);
        setHeight(data.height);
        setWeight(data.weight);
        setEgg(data.egg);
        nameInput.current.focus();


    };

    useEffect(() => {
        getData2();
    }, []);

    return (
        <div className="row">
            <div className="col-md-4">
                <form onSubmit={handleSubmit} className="card card-body">
                    <div className="form-group">
                        <input
                            type="text"
                            onChange={(e) => setName(e.target.value)}
                            value={name}
                            className="form-control"
                            placeholder="name"
                            ref={nameInput}
                            autoFocus
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="text"
                            onChange={(e) => setHeight(e.target.value)}
                            value={height}
                            className="form-control"
                            placeholder="height"
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="text"
                            onChange={(e) => setWeight(e.target.value)}
                            value={weight}
                            className="form-control"
                            placeholder="weight"
                        />
                    </div>
                    <div className="form-group">
                        <input
                            type="text"
                            onChange={(e) => setEgg(e.target.value)}
                            value={egg}
                            className="form-control"
                            placeholder="egg"
                        />
                    </div>
                    <button className="btn btn-primary btn-block">
                        {editing ? "Update" : "Create"}
                    </button>
                </form>
            </div>
            <div className="col-md-6">
                <table className="table table-striped">
                    <thead>
                        <tr>
                            <th>name</th>
                            <th>height</th>
                            <th>weight</th>
                            <th>egg</th>
                        </tr>
                    </thead>
                    <tbody>
                        {data2.map((dat) => (
                            <tr key={dat._id}>
                                <td>{dat.name}</td>
                                <td>{dat.height}</td>
                                <td>{dat.weight}</td>
                                <td>{dat.egg}</td>
                                <td>
                                    <button
                                        className="btn btn-secondary btn-sm btn-block"
                                        onClick={(e) => editDat(dat._id)}
                                    >
                                        Edit
                                    </button>
                                    <button
                                        className="btn btn-danger btn-sm btn-block"
                                        onClick={(e) => deleteDat(dat._id)}
                                    >
                                        Delete
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};